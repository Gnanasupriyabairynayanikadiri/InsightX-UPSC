# =========================================================
# FILE: core/progress_dashboard.py
# SMART UPSC PROGRESS DASHBOARD
# =========================================================

import streamlit as st

from core.progress import (
    get_detailed_progress,
    is_completed
)

from core.xp import (
    get_user_stats,
    get_level,
    get_rank
)

from core.quiz_analytics import (
    get_quiz_stats,
    get_weak_chapters,
    get_strong_chapters
)

from core.mcq_analytics import (
    get_mcq_stats,
    get_weak_topics,
    get_strong_topics
)

from core.answer_analytics import (
    get_answer_stats,
    get_weak_topics as get_weak_answer_topics,
    get_strong_topics as get_strong_answer_topics
)

from data.ncert_quiz import ncert_quiz




# =========================================================
# DASHBOARD UI
# =========================================================

def progress_dashboard_ui(user):

    st.title("📊 Smart Progress Dashboard")

    # =====================================================
    # LOAD DATA
    # =====================================================

    analytics = get_detailed_progress(
        user,
        ncert_quiz
    )

    user_stats = get_user_stats(user)

    quiz_stats = get_quiz_stats(user)

    mcq_stats = get_mcq_stats(user)

    answer_stats = get_answer_stats(user)

    xp = user_stats.get(
        "xp",
        0
    )

    streak = user_stats.get(
        "streak",
        0
    )

    level = get_level(xp)

    rank = get_rank(user)

    # =====================================================
    # PERFORMANCE OVERVIEW
    # =====================================================

    st.markdown(
        "## 🏆 Performance Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "⭐ XP",
            xp
        )

    with c2:
        st.metric(
            "🏅 Level",
            level
        )

    with c3:
        st.metric(
            "🔥 Streak",
            streak
        )

    with c4:
        st.metric(
            "🏆 Rank",
            rank if rank else "-"
        )

    st.divider()

    # =====================================================
    # NCERT PROGRESS
    # =====================================================

    st.markdown(
        "## 📚 NCERT Progress"
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

    st.progress(
        overall / 100
        if overall
        else 0
    )

    st.info(
        f"""
Completed Chapters: {done}

Remaining Chapters: {max(total-done,0)}

Completion: {overall}%
"""
    )

    st.divider()

    # =====================================================
    # SUBJECT PROGRESS
    # =====================================================

    st.markdown(
        "## 📖 Subject Wise Progress"
    )

    subjects = analytics.get(
        "subjects",
        {}
    )

    for subject, stats in subjects.items():

        percent = stats.get(
            "percent",
            0
        )

        st.markdown(
            f"### {subject} ({percent}%)"
        )

        st.progress(
            percent / 100
        )

        st.write(
            f"{stats.get('done',0)} / {stats.get('total',0)} chapters completed"
        )

    st.divider()

    # =====================================================
    # QUIZ PERFORMANCE
    # =====================================================

    st.markdown(
        "## 📝 Quiz Performance"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Attempts",
            quiz_stats.get(
                "attempts",
                0
            )
        )

    with c2:

        st.metric(
            "Average Score",
            f"{quiz_stats.get('average_score',0)}%"
        )

    with c3:

        st.metric(
            "Highest Score",
            f"{quiz_stats.get('highest_score',0)}%"
        )

    weak_chapters = get_weak_chapters(
        user
    )

    if weak_chapters:

        st.warning(
            "⚠️ Weak Chapters"
        )

        for item in weak_chapters:

            st.write(
                f"{item.get('subject','Unknown')} → {item.get('chapter','Unknown')} ({item.get('percentage',0)}%)"
            )

    strong_chapters = get_strong_chapters(
        user
    )

    if strong_chapters:

        st.success(
            "🏆 Strong Chapters"
        )

        for item in strong_chapters:

            st.write(
                 f"{item.get('subject','Unknown')} → {item.get('chapter','Unknown')} ({item.get('percentage',0)}%)"
            )

    st.divider()

    # =====================================================
    # MCQ PERFORMANCE
    # =====================================================

    st.markdown(
        "## 🎯 MCQ Performance"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Attempts",
            mcq_stats.get(
                "attempts",
                0
            )
        )

    with c2:

        st.metric(
            "Accuracy",
            f"{mcq_stats.get('average_accuracy',0)}%"
        )

    with c3:

        st.metric(
            "Highest Accuracy",
            f"{mcq_stats.get('highest_accuracy',0)}%"
        )

    weak_topics = get_weak_topics(
        user
    )

    if weak_topics:

        st.warning(
            "⚠️ Weak MCQ Topics"
        )

        for item in weak_topics:

            st.write(
                f"{item['subject']} → {item['chapter']} ({item['accuracy']}%)"
            )

    strong_topics = get_strong_topics(
        user
    )

    if strong_topics:

        st.success(
            "🏆 Strong MCQ Topics"
        )

        for item in strong_topics:

            st.write(
                f"{item['subject']} → {item['chapter']} ({item['accuracy']}%)"
            )

    st.divider()

    # =====================================================
    # ANSWER WRITING
    # =====================================================

    st.markdown(
        "## ✍️ Answer Writing"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Answers Written",
            answer_stats.get(
                "attempts",
                0
            )
        )

    with c2:

        st.metric(
            "Average Score",
            answer_stats.get(
                "average_score",
                0
            )
        )

    with c3:

        st.metric(
            "Highest Score",
            answer_stats.get(
                "highest_score",
                0
            )
        )

    weak_answers = get_weak_answer_topics(
        user
    )

    if weak_answers:

        st.warning(
            "⚠️ Weak Answer Writing Topics"
        )

        for item in weak_answers:

            st.write(
                f"{item['subject']} → {item['chapter']} ({item['percentage']}%)"
            )

    strong_answers = get_strong_answer_topics(
        user
    )

    if strong_answers:

        st.success(
            "🏆 Strong Answer Writing Topics"
        )

        for item in strong_answers:

            st.write(
                f"{item['subject']} → {item['chapter']} ({item['percentage']}%)"
            )

    st.divider()

    # =====================================================
    # REVISION RECOMMENDATIONS
    # =====================================================

    st.markdown(
        "## 📈 Revision Recommendations"
    )
    for item in weak_answers[:3]:

        st.warning(
            f"Practice Answer Writing → {item['chapter']}"
        )

    st.divider()

    # =====================================================
    # DAILY TARGET
    # =====================================================

    daily_target = min(
        max(total - done, 0),
        5
    )

    st.info(
        f"🎯 Daily Target: Complete {daily_target} chapter(s)"
    )

    # =====================================================
    # MOTIVATION
    # =====================================================

    st.markdown(
        "## 🔥 Motivation"
    )

    if overall >= 90:

        st.success(
            "🏆 UPSC Beast Mode Activated!"
        )

    elif overall >= 75:

        st.success(
            "🔥 Excellent consistency!"
        )

    elif overall >= 50:

        st.info(
            "🚀 Strong progress!"
        )

    elif overall >= 25:

        st.warning(
            "⚡ Keep building momentum!"
        )

    else:

        st.error(
            "📚 Start small. Stay consistent."
        )

    st.success(
        "💡 Consistency beats intensity in UPSC preparation."
    )