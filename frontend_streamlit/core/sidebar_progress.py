# ==============================
# 📁 FILE: core/sidebar_progress.py
# PREMIUM UPSC SIDEBAR DASHBOARD
# ==============================

import streamlit as st

from core.progress import get_detailed_progress
from data.ncert_quiz import ncert_quiz
from data.csat_data import csat_data


# ==============================
# 📘 TOTAL NCERT CHAPTERS
# ==============================
def get_total_ncert_chapters():

    total = 0

    for subject in ncert_quiz.values():

        if not isinstance(subject, dict):
            continue

        for cls in subject.values():

            if isinstance(cls, dict):
                total += len(cls)

    return total


# ==============================
# 🧠 TOTAL CSAT QUESTIONS
# ==============================
def get_total_csat_questions():

    total = 0

    try:

        for section in csat_data.values():

            if not isinstance(section, dict):
                continue

            for topic in section.values():

                if not isinstance(topic, dict):
                    continue

                for level in topic.values():

                    if isinstance(level, list):
                        total += len(level)

    except Exception:

        return 0

    return total


# ==============================
# 🏆 GET USER LEVEL TITLE
# ==============================
def get_level_title(level):

    if level >= 50:
        return "👑 UPSC Legend"

    elif level >= 40:
        return "🔥 Civil Services Master"

    elif level >= 30:
        return "⚔️ UPSC Warrior"

    elif level >= 20:
        return "🚀 Advanced Aspirant"

    elif level >= 10:
        return "📚 Serious Aspirant"

    return "🌱 Beginner Aspirant"


# ==============================
# 🎯 MOTIVATION MESSAGE
# ==============================
def get_motivation(overall):

    if overall >= 90:
        return "🏆 You're Prelims Ready!"

    elif overall >= 75:
        return "🔥 Excellent consistency!"

    elif overall >= 60:
        return "🚀 Great momentum!"

    elif overall >= 40:
        return "⚡ Keep pushing daily!"

    elif overall >= 20:
        return "📘 Build consistency!"

    return "🌱 Start strong today!"


# ==============================
# 📊 MAIN SIDEBAR UI
# ==============================
def sidebar_progress_ui(user):

    # ==============================
    # USER SAFE ACCESS
    # ==============================
    if not isinstance(user, dict):

        user = {
            "username": "Aspirant",
            "xp": 0,
            "level": 1,
            "streak": 0
        }

    username = user.get(
        "username",
        "Aspirant"
    )

    xp = user.get(
        "xp",
        0
    )

    level = user.get(
        "level",
        1
    )

    streak = user.get(
        "streak",
        0
    )

    # ==============================
    # HEADER
    # ==============================
    st.sidebar.markdown(
        """
        <h1 style='text-align:center; color:#ff4b4b;'>
        🚀 InsightX
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ==============================
    # USER CARD
    # ==============================
    st.sidebar.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#111827,#1f2937);
            padding:18px;
            border-radius:18px;
            border:1px solid #374151;
            margin-bottom:15px;
        ">

        <h3 style='color:white; margin-bottom:5px;'>
        👤 {username}
        </h3>

        <p style='color:#9ca3af; margin-top:0px;'>
        {get_level_title(level)}
        </p>

        <hr style='border:0.5px solid #374151;'>

        <p style='color:#fbbf24;'>
        ⭐ XP: <b>{xp}</b>
        </p>

        <p style='color:#60a5fa;'>
        🏆 Level: <b>{level}</b>
        </p>

        <p style='color:#f97316;'>
        🔥 Streak: <b>{streak}</b> days
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ==============================
    # NCERT PROGRESS
    # ==============================
    try:

        analytics = get_detailed_progress(
            user,
            ncert_quiz
        )

        overall = analytics.get(
            "overall",
            0
        )

        done = analytics.get(
            "done",
            0
        )

        total = analytics.get(
            "total",
            0
        )

    except Exception:

        overall = 0
        done = 0
        total = get_total_ncert_chapters()

    st.sidebar.markdown("## 📖 NCERT Progress")

    st.sidebar.progress(overall / 100)

    st.sidebar.caption(
        f"{overall}% Complete ({done}/{total})"
    )

    # ==============================
    # CORE SUBJECTS
    # ==============================
    st.sidebar.markdown("## 🎯 Core Subjects")

    core_progress = st.session_state.get(
        "core_progress",
        0
    )

    st.sidebar.progress(core_progress / 100)

    st.sidebar.caption(
        f"{core_progress}% Complete"
    )

    # ==============================
    # CSAT
    # ==============================
    st.sidebar.markdown("## ➗ CSAT Progress")

    total_questions = get_total_csat_questions()

    solved = st.session_state.get(
        "csat_solved",
        0
    )

    percent = (
        int((solved / total_questions) * 100)
        if total_questions else 0
    )

    st.sidebar.progress(percent / 100)

    st.sidebar.caption(
        f"{percent}% Complete ({solved}/{total_questions})"
    )

    # ==============================
    # DAILY TARGET
    # ==============================
    remaining = max(total - done, 0)

    daily_target = min(5, remaining)

    st.sidebar.markdown("---")

    st.sidebar.info(
        f"🎯 Daily Target: {daily_target} chapter(s)"
    )

    # ==============================
    # MOTIVATION
    # ==============================
    st.sidebar.markdown("---")

    motivation = get_motivation(overall)

    if overall >= 75:

        st.sidebar.success(motivation)

    elif overall >= 40:

        st.sidebar.info(motivation)

    else:

        st.sidebar.warning(motivation)

    # ==============================
    # QUICK STATS
    # ==============================
    st.sidebar.markdown("---")

    st.sidebar.markdown("## ⚡ Quick Stats")

    total_quiz = st.session_state.get(
        "total_quiz_attempted",
        0
    )

    total_correct = st.session_state.get(
        "total_correct_answers",
        0
    )

    accuracy = (
        int((total_correct / total_quiz) * 100)
        if total_quiz else 0
    )

    st.sidebar.markdown(
        f"""
        ✅ Correct Answers: **{total_correct}**

        📝 Quiz Attempted: **{total_quiz}**

        🎯 Accuracy: **{accuracy}%**
        """
    )

    # ==============================
    # PRELIMS READINESS
    # ==============================
    st.sidebar.markdown("---")

    readiness = int(
        (overall + core_progress + percent) / 3
    )

    st.sidebar.markdown("## 🏁 Prelims Readiness")

    st.sidebar.progress(readiness / 100)

    st.sidebar.caption(
        f"{readiness}% UPSC Readiness"
    )

    # ==============================
    # FOOTER
    # ==============================
    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
        <div style='text-align:center; color:gray; font-size:12px;'>

        Built for UPSC Aspirants ❤️

        InsightX AI Learning Platform

        </div>
        """,
        unsafe_allow_html=True
    )