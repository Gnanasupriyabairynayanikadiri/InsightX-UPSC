# =========================================================
# 📁 FILE: core/analytics_ui.py
# UPSC ANALYTICS DASHBOARD UI
# =========================================================

import streamlit as st

from core.analytics import (
    get_full_analytics,
    get_user_summary
)


# =========================================================
# MAIN UI
# =========================================================
def analytics_ui(user="guest"):

    st.title("📊 UPSC Performance Analytics")

    st.caption("Track your preparation, improvement, and weak areas")

    analytics = get_full_analytics(user)
    summary = get_user_summary(user)

    # =====================================================
    # SUMMARY CARDS
    # =====================================================
    st.markdown("## 🧬 Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Total Answers", summary["answers"])

    with col2:
        st.metric("📊 Average Score", summary["average"])

    with col3:
        st.metric("🏆 Rank", summary["rank"])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("🔥 XP", summary["xp"])

    with col5:
        st.metric("⚡ Streak", summary["streak"])

    with col6:
        st.metric("📘 Performance", summary["label"])

    st.markdown("---")

    # =====================================================
    # STRONG / WEAK SUBJECT
    # =====================================================
    st.markdown("## 📚 Subject Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"💪 Strongest Subject: {summary['best_subject']}")

    with col2:
        st.warning(f"⚠️ Weakest Subject: {summary['weak_subject']}")

    st.markdown("---")

    # =====================================================
    # IMPROVEMENT TREND
    # =====================================================
    st.markdown("## 📈 Improvement Trend")

    trend = analytics["improvement"]

    if trend["improved"]:
        st.success(f"📈 You are improving by +{trend['difference']} avg score")
    else:
        st.error(f"📉 Drop detected: {trend['difference']} avg score")

    st.markdown("---")

    # =====================================================
    # SUBJECT WISE ANALYTICS
    # =====================================================
    st.markdown("## 📊 Subject-wise Performance")

    subject_data = analytics["subject_wise"]

    if not subject_data:
        st.info("No subject data available yet")
    else:

        for subject, data in subject_data.items():

            st.markdown(f"### 📘 {subject}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average", data["average"])

            with col2:
                st.metric("Attempts", data["attempts"])

            with col3:
                st.metric("Highest", data["highest"])

            with col4:
                st.metric("Lowest", data["lowest"])

            st.markdown("---")

    # =====================================================
    # SCORE DISTRIBUTION
    # =====================================================
    st.markdown("## 📉 Score Distribution")

    dist = analytics["distribution"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("0-3", dist["0-3"])

    with col2:
        st.metric("4-5", dist["4-5"])

    with col3:
        st.metric("6-7", dist["6-7"])

    with col4:
        st.metric("8-10", dist["8-10"])

    st.markdown("---")

    # =====================================================
    # RECENT PERFORMANCE
    # =====================================================
    st.markdown("## 🧠 Recent Answers")

    recent = analytics["recent"]

    if not recent:
        st.info("No recent answers found")
    else:

        for r in recent:

            st.markdown(
                f"""
                **📘 Subject:** {r.get('subject', 'Unknown')}  
                **📊 Score:** {r.get('score', 0)}  
                **📝 Answer:** {r.get('answer', '')[:120]}...
                """
            )

            st.markdown("---")

    # =====================================================
    # XP / GAMIFICATION SECTION
    # =====================================================
    st.markdown("## 🏅 Gamification Stats")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"🔥 XP: {analytics['xp']}")

    with col2:
        st.info(f"🏆 Rank: {analytics['rank']}")

    with col3:
        st.warning(f"⚡ Streak: {analytics['streak']}")

    # =====================================================
    # FINAL MESSAGE
    # =====================================================
    st.markdown("---")

    if summary["average"] >= 8:
        st.success("🏆 Excellent performance! You are UPSC ready level.")
    elif summary["average"] >= 6:
        st.info("🔥 Good progress — focus on consistency.")
    else:
        st.warning("⚡ Focus on improvement — revise fundamentals daily.")