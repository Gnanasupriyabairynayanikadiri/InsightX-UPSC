# =========================================================
# 📁 FILE: core/dashboard.py
# =========================================================

import streamlit as st

from core.xp import (
    get_xp,
    get_level,
    get_streak,
    get_rank
)


# =========================================================
# SAMPLE USER STATS DATABASE
# =========================================================
USER_STATS = {

    "answers_written": 24,

    "average_score": 6.8,

    "best_score": 9,

    "current_affairs_read": 18,

    "mcqs_practiced": 240,

    "study_hours": 72,

    "strong_subject": "Art & Culture",

    "weak_subject": "Economy"
}


# =========================================================
# PROGRESS BAR
# =========================================================
def progress_bar(value):

    st.progress(value)


# =========================================================
# PERFORMANCE STATUS
# =========================================================
def performance_status(score):

    if score >= 8:

        return "🔥 Excellent"

    elif score >= 6:

        return "👍 Good"

    elif score >= 4:

        return "⚠️ Average"

    return "❌ Needs Improvement"


# =========================================================
# DASHBOARD UI
# =========================================================
def dashboard_ui(username):

    st.title("📊 UPSC AI Dashboard")

    st.markdown("---")


    # =====================================================
    # USER DETAILS
    # =====================================================
    xp = get_xp(username)

    level = get_level(username)

    streak = get_streak(username)

    rank = get_rank(username)


    # =====================================================
    # TOP METRICS
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "⭐ XP",

            xp
        )

    with col2:

        st.metric(

            "🏆 Level",

            level
        )

    with col3:

        st.metric(

            "🔥 Streak",

            streak
        )

    with col4:

        st.metric(

            "🎯 Rank",

            rank
        )


    st.markdown("---")


    # =====================================================
    # ANSWER WRITING ANALYTICS
    # =====================================================
    st.subheader("✍️ Answer Writing Analytics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Answers Written",

            USER_STATS["answers_written"]
        )

    with col2:

        st.metric(

            "Average Score",

            USER_STATS["average_score"]
        )

    with col3:

        st.metric(

            "Best Score",

            USER_STATS["best_score"]
        )


    # =====================================================
    # PERFORMANCE STATUS
    # =====================================================
    status = performance_status(

        USER_STATS["average_score"]
    )

    st.success(

        f"Performance Status: {status}"
    )


    # =====================================================
    # PROGRESS
    # =====================================================
    st.markdown("### 📈 UPSC Readiness Progress")

    readiness = int(

        USER_STATS["average_score"] * 10
    )

    progress_bar(readiness)

    st.write(

        f"{readiness}% UPSC Ready"
    )


    st.markdown("---")


    # =====================================================
    # SUBJECT ANALYSIS
    # =====================================================
    st.subheader("📚 Subject Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.success(

            f"✅ Strong Subject: {USER_STATS['strong_subject']}"
        )

    with col2:

        st.error(

            f"⚠️ Weak Subject: {USER_STATS['weak_subject']}"
        )


    st.markdown("---")


    # =====================================================
    # CURRENT AFFAIRS STATS
    # =====================================================
    st.subheader("📰 Current Affairs Stats")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Articles Read",

            USER_STATS["current_affairs_read"]
        )

    with col2:

        st.metric(

            "MCQs Practiced",

            USER_STATS["mcqs_practiced"]
        )


    st.markdown("---")


    # =====================================================
    # STUDY TRACKER
    # =====================================================
    st.subheader("⏳ Study Tracker")

    study_hours = USER_STATS["study_hours"]

    st.info(

        f"Total Study Hours: {study_hours} hrs"
    )

    hours_progress = min(

        int((study_hours / 100) * 100),

        100
    )

    progress_bar(hours_progress)


    st.markdown("---")


    # =====================================================
    # AI INSIGHTS
    # =====================================================
    st.subheader("🤖 AI Insights")

    insights = []

    avg_score = USER_STATS["average_score"]

    if avg_score >= 8:

        insights.append(

            "Excellent answer writing consistency."
        )

    elif avg_score >= 6:

        insights.append(

            "Good progress in answer writing."
        )

    else:

        insights.append(

            "Focus more on answer structure and relevance."
        )

    insights.append(

        f"Improve performance in {USER_STATS['weak_subject']}."
    )

    insights.append(

        "Practice more analytical answers for higher scores."
    )

    insights.append(

        "Maintain daily answer writing consistency."
    )

    for item in insights:

        st.write(f"• {item}")


    st.markdown("---")


    # =====================================================
    # DAILY MOTIVATION
    # =====================================================
    st.subheader("🌟 Daily Motivation")

    st.success(

        """
Consistency beats intensity.

Small daily improvements in answer writing,
current affairs, and revision will compound into UPSC success.
"""
    )


    st.markdown("---")


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================
    st.subheader("🚀 Recommended Tasks")

    tasks = [

        "Write 2 GS answers today",

        "Revise current affairs",

        "Practice 25 MCQs",

        "Improve weak subject areas",

        "Focus on conclusion writing"
    ]

    for task in tasks:

        st.write(f"✅ {task}")