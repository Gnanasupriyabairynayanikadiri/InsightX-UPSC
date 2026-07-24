# =========================================================
# 📁 FILE: core/map_ui.py
# AI UPSC MAP UI ENGINE
# =========================================================

import streamlit as st

from core.map_engine import (
    generate_map_question,
    evaluate_answer,
    get_question_explanation,
    generate_score_analysis,
    get_difficulty_color
)

from core.map_xp_engine import (
    reward_map_user,
    get_map_analytics,
    get_map_leaderboard,
    get_geo_mastery_level,
    generate_daily_map_challenge
)

from core.map_visual_engine import (
    show_world_map,
    show_india_map,
    show_geopolitical_map
)


# =========================================================
# 🗺️ MAIN MAP UI
# =========================================================
def map_ui(user="guest"):

    st.title("🗺️ AI UPSC Map Intelligence")

    st.caption(
        "Interactive Geography + Mapping + Geopolitics Practice"
    )

    st.markdown("---")

    # =====================================================
    # DAILY CHALLENGE
    # =====================================================
    st.success(
        f"🎯 Daily Challenge: "
        f"{generate_daily_map_challenge()}"
    )

    st.markdown("---")

    # =====================================================
    # TABS
    # =====================================================
    tab1, tab2, tab3, tab4 = st.tabs([

        "🧠 Quiz",

        "🗺️ Maps",

        "📊 Analytics",

        "🏆 Leaderboard"
    ])

    # =====================================================
    # 🧠 QUIZ TAB
    # =====================================================
    with tab1:

        show_quiz_tab(user)

    # =====================================================
    # 🗺️ MAP TAB
    # =====================================================
    with tab2:

        show_maps_tab()

    # =====================================================
    # 📊 ANALYTICS TAB
    # =====================================================
    with tab3:

        show_analytics_tab(user)

    # =====================================================
    # 🏆 LEADERBOARD
    # =====================================================
    with tab4:

        show_leaderboard_tab()


# =========================================================
# 🧠 QUIZ TAB
# =========================================================
def show_quiz_tab(user):

    # =====================================================
    # CATEGORY SELECTOR
    # =====================================================
    category = st.selectbox(

        "🌍 Select Topic",

        [

            "Mixed",

            "World Capitals",

            "World Continents",

            "World Rivers",

            "World Mountains",

            "World Straits",

            "Indian States",

            "Indian Rivers",

            "Indian Mountains",

            "Geopolitics"
        ]
    )

    st.markdown("---")

    # =====================================================
    # SESSION STATE
    # =====================================================
    if "map_question" not in st.session_state:

        st.session_state.map_question = (
            generate_map_question(category)
        )

    if "map_category" not in st.session_state:

        st.session_state.map_category = category

    # =====================================================
    # CATEGORY CHANGED
    # =====================================================
    if st.session_state.map_category != category:

        st.session_state.map_question = (
            generate_map_question(category)
        )

        st.session_state.map_category = category

    question = st.session_state.map_question

    # =====================================================
    # QUESTION
    # =====================================================
    difficulty_icon = get_difficulty_color(

        question["difficulty"]
    )

    st.markdown(

        f"### {difficulty_icon} "
        f"{question['question']}"
    )

    st.caption(
        f"📘 Topic: {question['topic']}"
    )

    choice = st.radio(

        "Choose Answer",

        question["options"]
    )

    # =====================================================
    # HINT
    # =====================================================
    with st.expander("💡 Hint"):

        st.info(question["hint"])

    # =====================================================
    # SUBMIT
    # =====================================================
    if st.button("✅ Submit Answer"):

        correct = evaluate_answer(

            choice,
            question["answer"]
        )

        # -------------------------------------------------
        # CORRECT
        # -------------------------------------------------
        if correct:

            st.success("🎉 Correct Answer!")

        else:

            st.error(

                f"❌ Wrong Answer\n\n"
                f"Correct Answer: "
                f"{question['answer']}"
            )

        # -------------------------------------------------
        # EXPLANATION
        # -------------------------------------------------
        st.info(

            get_question_explanation(question)
        )

        # -------------------------------------------------
        # XP SYSTEM
        # -------------------------------------------------
        reward = reward_map_user(

            user=user,

            correct=correct,

            category=category.lower(),

            difficulty=question["difficulty"]
        )

        # -------------------------------------------------
        # REWARD DISPLAY
        # -------------------------------------------------
        st.success(

            f"⭐ +{reward['xp_gained']} XP | "
            f"🏆 Level {reward['level']}"
        )

    # =====================================================
    # NEXT QUESTION
    # =====================================================
    if st.button("🔄 Next Question"):

        st.session_state.map_question = (
            generate_map_question(category)
        )

        st.rerun()


# =========================================================
# 🗺️ MAP TAB
# =========================================================
def show_maps_tab():

    map_type = st.selectbox(

        "🗺️ Select Map",

        [

            "World Map",

            "India Map",

            "Geopolitical Hotspots"
        ]
    )

    st.markdown("---")

    if map_type == "World Map":

        show_world_map()

    elif map_type == "India Map":

        show_india_map()

    else:

        show_geopolitical_map()


# =========================================================
# 📊 ANALYTICS TAB
# =========================================================
def show_analytics_tab(user):

    analytics = get_map_analytics(user)

    st.subheader("📊 Progress Dashboard")

    st.markdown("---")

    # =====================================================
    # METRICS
    # =====================================================
    col1, col2, col3 = st.columns(3)

    col1.metric(

        "🏆 XP",

        analytics["xp"]
    )

    col2.metric(

        "🎯 Accuracy",

        f"{analytics['accuracy']}%"
    )

    col3.metric(

        "🔥 Current Streak",

        analytics["streak"]
    )

    st.markdown("---")

    # =====================================================
    # LEVEL
    # =====================================================
    st.subheader("🎖️ Level")

    st.success(

        f"Level {analytics['level']}"
    )

    # =====================================================
    # BADGES
    # =====================================================
    st.subheader("🏅 Achievements")

    if analytics["badges"]:

        for badge in analytics["badges"]:

            st.success(f"✅ {badge}")

    else:

        st.info("No badges unlocked yet.")

    # =====================================================
    # MASTERY
    # =====================================================
    st.subheader("🌍 Topic Mastery")

    mastery = analytics["geo_mastery"]

    for topic, points in mastery.items():

        level = get_geo_mastery_level(points)

        st.write(

            f"📘 {topic.title()} → "
            f"{level} ({points} pts)"
        )


# =========================================================
# 🏆 LEADERBOARD
# =========================================================
def show_leaderboard_tab():

    leaderboard = get_map_leaderboard()

    st.subheader("🏆 Top Players")

    st.markdown("---")

    rank = 1

    for player in leaderboard:

        st.write(

            f"{rank}. "
            f"{player['user']} "
            f"⭐ {player['xp']} XP "
            f"(Level {player['level']})"
        )

        rank += 1