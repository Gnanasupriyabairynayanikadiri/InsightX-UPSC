# core/daily_ui.py

import streamlit as st
import json
import os

from datetime import date

from core.daily import get_today_question
from core.xp import (
    add_xp,
    update_streak
)

# ==============================
# FILE
# ==============================
FILE = "storage/daily_mcq.json"


# ==============================
# LOAD DATA
# ==============================
def load_data():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except Exception:
        return {}


# ==============================
# SAVE DATA
# ==============================
def save_data(data):

    os.makedirs("storage", exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# CHECK ATTEMPT
# ==============================
def already_attempted(user, today, data):

    return (
        user in data and
        today in data[user]
    )


# ==============================
# SAVE ATTEMPT
# ==============================
def save_attempt(
    user,
    today,
    question,
    selected,
    correct,
    xp
):

    data = load_data()

    if user not in data:
        data[user] = {}

    data[user][today] = {

        "question": question["question"],

        "selected": selected,

        "correct_answer": question["answer"],

        "is_correct": correct,

        "xp": xp
    }

    save_data(data)


# ==============================
# LEADERBOARD
# ==============================
def show_leaderboard(today):

    st.markdown("## 🏆 Daily Leaderboard")

    data = load_data()

    board = []

    for user, attempts in data.items():

        if today in attempts:

            entry = attempts[today]

            board.append({
                "user": user,
                "xp": entry["xp"],
                "correct": entry["is_correct"]
            })

    if not board:

        st.info("No attempts yet.")
        return

    board = sorted(
        board,
        key=lambda x: x["xp"],
        reverse=True
    )

    for i, row in enumerate(board[:10], start=1):

        medal = ""

        if i == 1:
            medal = "🥇"

        elif i == 2:
            medal = "🥈"

        elif i == 3:
            medal = "🥉"

        status = "✅" if row["correct"] else "❌"

        st.write(
            f"{medal} {i}. {row['user']} — {row['xp']} XP {status}"
        )


# ==============================
# MAIN UI
# ==============================
def daily_ui(username):

    st.title("📅 Daily MCQ Challenge")

    today = str(date.today())

    question = get_today_question()

    data = load_data()

    # ==============================
    # QUESTION CARD
    # ==============================
    st.markdown("## 🎯 Today's Question")

    if isinstance(question, dict):

        if "subject" in question:
            st.info(f"📘 Subject: {question['subject']}")

        if "level" in question:
            st.info(f"🎯 Level: {question['level']}")

    st.markdown("---")

    st.subheader(question["question"])

    # ==============================
    # ALREADY ATTEMPTED
    # ==============================
    if already_attempted(username, today, data):

        st.success(
            "✅ You already attempted today's challenge."
        )

        previous = data[username][today]

        st.write(
            f"🖊️ Your Answer: {previous['selected']}"
        )

        st.write(
            f"✅ Correct Answer: {previous['correct_answer']}"
        )

        if previous["is_correct"]:

            st.success("🎉 Correct Answer")

        else:

            st.error("❌ Wrong Answer")

        st.write(f"⭐ XP Earned: {previous['xp']}")

        st.markdown("---")

        show_leaderboard(today)

        return

    # ==============================
    # OPTIONS
    # ==============================
    selected = st.radio(
        "Choose Answer",
        question["options"]
    )

    # ==============================
    # SUBMIT
    # ==============================
    if st.button("🚀 Submit Answer"):

        correct = selected == question["answer"]

        # ==============================
        # CORRECT
        # ==============================
        if correct:

            xp = 20

            st.success(
                "✅ Correct Answer!"
            )

            st.balloons()

        # ==============================
        # WRONG
        # ==============================
        else:

            xp = 5

            st.error(
                f"❌ Wrong Answer"
            )

            st.info(
                f"✅ Correct Answer: {question['answer']}"
            )

        # ==============================
        # EXPLANATION
        # ==============================
        if "explanation" in question:

            st.markdown("## 🧠 Explanation")

            st.info(question["explanation"])

        # ==============================
        # XP
        # ==============================
        add_xp(username, xp)

        streak = update_streak(username)

        st.success(
            f"⭐ XP Earned: {xp}"
        )

        st.success(
            f"🔥 Streak: {streak} days"
        )

        # ==============================
        # SAVE
        # ==============================
        save_attempt(
            username,
            today,
            question,
            selected,
            correct,
            xp
        )

        st.markdown("---")

        st.info(
            "🎯 Come back tomorrow for a new challenge!"
        )

        # ==============================
        # LEADERBOARD
        # ==============================
        show_leaderboard(today)