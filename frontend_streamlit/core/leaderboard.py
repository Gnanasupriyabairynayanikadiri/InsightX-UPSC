# =========================================================
# 📁 FILE: core/leaderboard.py
# =========================================================

import streamlit as st

from core.xp import (

    get_leaderboard,

    get_xp,

    get_level,

    get_streak,

    get_rank
)


# =========================================================
# LEADERBOARD HEADER
# =========================================================
def leaderboard_header():

    st.title("🏆 UPSC AI Leaderboard")

    st.markdown(
        """
Compete with aspirants through:
- XP Points
- Daily Streaks
- Answer Writing
- Quiz Practice
- Current Affairs Consistency
"""
    )

    st.markdown("---")


# =========================================================
# RANK BADGES
# =========================================================
def get_rank_badge(position):

    if position == 1:

        return "🥇"

    elif position == 2:

        return "🥈"

    elif position == 3:

        return "🥉"

    return "🏅"


# =========================================================
# PERFORMANCE TAG
# =========================================================
def get_performance_tag(xp):

    if xp >= 5000:

        return "🔥 UPSC Beast"

    elif xp >= 3000:

        return "🚀 Top Performer"

    elif xp >= 1500:

        return "⚡ Consistent Learner"

    elif xp >= 500:

        return "📘 Active Aspirant"

    return "🌱 Beginner"


# =========================================================
# USER CARD
# =========================================================
def show_user_card(user, position):

    badge = get_rank_badge(position)

    performance = get_performance_tag(user["xp"])

    with st.container():

        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])

        with col1:

            st.markdown(f"## {badge}")

        with col2:

            st.markdown(f"### {user['name']}")

            st.caption(performance)

        with col3:

            st.metric(

                "⭐ XP",

                user["xp"]
            )

        with col4:

            st.metric(

                "🏆 Level",

                user["level"]
            )

        with col5:

            st.metric(

                "🔥 Streak",

                user["streak"]
            )

        st.markdown("---")


# =========================================================
# TOPPER MESSAGE
# =========================================================
def topper_message():

    messages = [

        "Consistency creates toppers.",

        "Daily answer writing builds UPSC confidence.",

        "Discipline beats motivation.",

        "Small improvements every day matter.",

        "Top ranks are earned through revision and practice."
    ]

    import random

    return random.choice(messages)


# =========================================================
# MAIN LEADERBOARD UI
# =========================================================
def leaderboard_ui(user=None):

    leaderboard_header()

    # =====================================================
    # GET DATA
    # =====================================================
    leaderboard = get_leaderboard()

    # =====================================================
    # EMPTY CHECK
    # =====================================================
    if len(leaderboard) == 0:

        st.warning("No leaderboard data available.")

        return

    # =====================================================
    # USER STATS
    # =====================================================
    if user:

        st.subheader("🙋 Your Performance")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "⭐ XP",

                get_xp(user)
            )

        with col2:

            st.metric(

                "🏆 Level",

                get_level(user)
            )

        with col3:

            st.metric(

                "🔥 Streak",

                get_streak(user)
            )

        with col4:

            st.metric(

                "🎯 Rank",

                get_rank(user)
            )

        st.markdown("---")

    # =====================================================
    # TOP 3 USERS
    # =====================================================
    st.subheader("👑 Top Performers")

    top_users = leaderboard[:3]

    for idx, player in enumerate(top_users):

        show_user_card(player, idx + 1)

    # =====================================================
    # FULL LEADERBOARD
    # =====================================================
    st.subheader("📊 Full Rankings")

    for idx, player in enumerate(leaderboard):

        badge = get_rank_badge(idx + 1)

        performance = get_performance_tag(player["xp"])

        with st.expander(

            f"{badge} Rank #{idx+1} - {player['name']}"
        ):

            st.write(f"⭐ XP: {player['xp']}")

            st.write(f"🏆 Level: {player['level']}")

            st.write(f"🔥 Streak: {player['streak']}")

            st.write(f"📈 Status: {performance}")

    st.markdown("---")

    # =====================================================
    # DAILY MOTIVATION
    # =====================================================
    st.subheader("🌟 Motivation")

    st.success(topper_message())

    st.markdown("---")

    # =====================================================
    # HOW TO IMPROVE
    # =====================================================
    st.subheader("🚀 How to Climb Leaderboard")

    tips = [

        "Write answers daily",

        "Practice MCQs consistently",

        "Revise current affairs regularly",

        "Maintain streaks",

        "Improve answer structure",

        "Use examples and analysis"
    ]

    for tip in tips:

        st.write(f"✅ {tip}")

    st.markdown("---")

    # =====================================================
    # AI ANALYSIS
    # =====================================================
    st.subheader("🤖 AI Leaderboard Insights")

    insights = [

        "Most toppers maintain daily answer writing consistency.",

        "Current affairs practice significantly boosts XP.",

        "Answer quality matters more than answer length.",

        "Maintaining streaks improves retention and discipline."
    ]

    for insight in insights:

        st.info(insight)

    st.markdown("---")

    # =====================================================
    # END MESSAGE
    # =====================================================
    st.success(

        """
UPSC preparation is not a sprint.
It is a long-term consistency game.

Keep improving daily.
"""
    )