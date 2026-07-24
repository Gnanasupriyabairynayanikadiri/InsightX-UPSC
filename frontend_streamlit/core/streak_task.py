# ==============================
# 📁 FILE: core/streak_task.py
# ==============================

import streamlit as st
import random
from datetime import date

from core.xp import (
    add_xp,
    update_streak,
    get_user_stats
)


# ==============================
# ❓ DAILY STREAK QUESTIONS
# ==============================
QUESTIONS = [

    {
        "q": "Who is the President of India?",
        "options": [
            "Narendra Modi",
            "Droupadi Murmu",
            "Rahul Gandhi",
            "Amit Shah"
        ],
        "ans": "Droupadi Murmu"
    },

    {
        "q": "Capital of India?",
        "options": [
            "Mumbai",
            "Delhi",
            "Chennai",
            "Kolkata"
        ],
        "ans": "Delhi"
    },

    {
        "q": "Earth is a?",
        "options": [
            "Star",
            "Planet",
            "Galaxy",
            "Asteroid"
        ],
        "ans": "Planet"
    },

    {
        "q": "Ganga River flows into?",
        "options": [
            "Arabian Sea",
            "Bay of Bengal",
            "Indian Ocean",
            "Pacific Ocean"
        ],
        "ans": "Bay of Bengal"
    },

    {
        "q": "Which Article deals with Right to Equality?",
        "options": [
            "Article 14",
            "Article 19",
            "Article 21",
            "Article 32"
        ],
        "ans": "Article 14"
    }
]


# ==============================
# 📅 GET TODAY KEY
# ==============================
def get_today():

    return str(date.today())


# ==============================
# ❓ GET TODAY QUESTION
# ==============================
def get_today_question():

    today = get_today()

    random.seed(today)

    return random.choice(QUESTIONS)


# ==============================
# 🔥 MAIN UI
# ==============================
def streak_task_ui(user):

    st.markdown("## 🔥 Daily Streak Task")

    today = get_today()

    # ==============================
    # 🚀 INIT SESSION
    # ==============================
    if "streak_done" not in st.session_state:
        st.session_state.streak_done = {}

    if "streak_score" not in st.session_state:
        st.session_state.streak_score = 0

    # ==============================
    # ✅ ALREADY COMPLETED
    # ==============================
    if st.session_state.streak_done.get(today):

        stats = get_user_stats(user)

        streak = stats.get("streak", 0)
        xp = stats.get("xp", 0)

        st.success("✅ Daily streak task completed!")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "🔥 Current Streak",
                f"{streak} Days"
            )

        with c2:
            st.metric(
                "⭐ Total XP",
                xp
            )

        return

    # ==============================
    # ❓ QUESTION
    # ==============================
    q = get_today_question()

    st.markdown(f"""
    <div style="
        background:#1E1E2F;
        padding:20px;
        border-radius:15px;
        margin-bottom:20px;
    ">
        <h3>🧠 {q['q']}</h3>
    </div>
    """, unsafe_allow_html=True)

    choice = st.radio(
        "Select Answer",
        q["options"],
        key="streak_choice"
    )

    # ==============================
    # 🚀 SUBMIT
    # ==============================
    if st.button("✅ Submit Task"):

        correct = choice == q["ans"]

        # ==============================
        # ⭐ XP REWARD
        # ==============================
        xp_reward = 5 if correct else 2

        add_xp(
            user,
            xp_reward
        )

        # ==============================
        # 🔥 UPDATE STREAK
        # ==============================
        streak = update_streak(user)

        # ==============================
        # 💬 FEEDBACK
        # ==============================
        if correct:

            st.success(
                "🎉 Correct Answer!"
            )

        else:

            st.error(
                f"❌ Wrong Answer"
            )

            st.info(
                f"✅ Correct Answer: {q['ans']}"
            )

        # ==============================
        # 📊 REWARDS
        # ==============================
        c1, c2 = st.columns(2)

        with c1:
            st.info(
                f"⭐ XP Earned: +{xp_reward}"
            )

        with c2:
            st.success(
                f"🔥 Streak: {streak} Days"
            )

        # ==============================
        # 💾 SAVE SESSION
        # ==============================
        st.session_state.streak_done[today] = True

        # ==============================
        # 🎯 MOTIVATION
        # ==============================
        st.markdown("---")

        if streak >= 30:

            st.success(
                "🏆 30+ Day Streak! UPSC Warrior!"
            )

        elif streak >= 15:

            st.success(
                "🔥 Amazing consistency!"
            )

        elif streak >= 7:

            st.info(
                "🚀 Great momentum!"
            )

        else:

            st.warning(
                "⚡ Build your daily habit!"
            )

        st.balloons()