import streamlit as st
import json
import os

# ---------------- CORE MODULES ----------------
from core.learning import learning_ui
from core.quiz_engine import quiz_ui
from core.current_affairs import current_affairs_ui
from core.answer_writing import answer_writing_ui
from core.map_practice import map_ui
from core.dictionary import dictionary_ui
from core.aptitude import aptitude_ui
from core.reasoning import reasoning_ui

from core.xp import (
    get_xp, get_level, get_streak,
    update_streak, get_daily_challenge,
    get_leaderboard, get_user_rank,
    get_subject_progress
)

from data.ncert_quiz import ncert_quiz

USERS_FILE = "storage/users.json"


# ---------------- USERS ----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    os.makedirs("storage", exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- AUTH ----------------
def register_ui():
    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    goal = st.selectbox("🎯 Goal", ["IAS", "IPS", "IFS", "IRS"])

    if st.button("Register"):
        users = load_users()

        if username in users:
            st.error("User already exists")
        else:
            users[username] = {
                "password": password,
                "goal": goal,
                "xp": 0,
                "streak": 0,
                "last_active": "",
                "challenge": [],
                "challenge_date": "",
                "completed": []
            }
            save_users(users)
            st.success("Registered! Please login.")


def login_ui():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()

        if username in users and users[username]["password"] == password:
            st.session_state.user = username
            update_streak(username)

            # 🔥 RESET QUIZ STATE
            for key in ["q_index", "score", "wrong", "start_time", "selected_path"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()
        else:
            st.error("Invalid credentials")


# ---------------- MAIN ----------------
def main():
    st.set_page_config(page_title="InsightX", layout="wide")

    # ---------------- UI STYLE ----------------
    st.markdown("""
    <style>
    body { background-color: #0E1117; }

    .card {
        background-color: #1E1E2F;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- LOGIN ----------------
    if "user" not in st.session_state:
        st.title("🚀 InsightX")
        choice = st.radio("Choose", ["Login", "Register"])

        if choice == "Login":
            login_ui()
        else:
            register_ui()
        return

    # ---------------- USER DATA ----------------
    user = st.session_state.user
    users = load_users()
    data = users.get(user, {})

    xp = get_xp(user)
    level = get_level(xp)
    streak = get_streak(user)
    goal = data.get("goal", "Aspirant")

    # ---------------- SIDEBAR ----------------
    st.sidebar.markdown("## 🚀 InsightX")
    st.sidebar.markdown(f"""
    <div class="card">
    👤 {user}<br>
    🎯 {goal}<br>
    ⭐ XP: {xp}<br>
    🏆 Level: {level}<br>
    🔥 Streak: {streak}
    </div>
    """, unsafe_allow_html=True)

    # ---------------- MENU ----------------
    MENU_OPTIONS = [
        "Home",
        "Learning",
        "Quiz",
        "Map Practice",
        "Dictionary",
        "Aptitude",
        "Reasoning",
        "Answer Writing",
        "Daily Challenge",
        "Current Affairs",
        "Leaderboard",
        "Logout"
    ]

    if "menu" not in st.session_state:
        st.session_state.menu = "Home"

    menu = st.sidebar.radio(
        "Navigation",
        MENU_OPTIONS,
        index=MENU_OPTIONS.index(st.session_state.menu)
    )

    st.session_state.menu = menu

    # ---------------- BREADCRUMB ----------------
    st.markdown(f"""
    <div class="card">
    📍 You are in: <b>{menu}</b>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- HOME ----------------
    if menu == "Home":
        st.title("🏠 Home")

        st.markdown(f"""
        <div class="card">
        👋 Welcome Future {goal} Officer
        </div>
        """, unsafe_allow_html=True)

        # Progress
        st.markdown("## 📊 Progress")
        subject_data = get_subject_progress(user, ncert_quiz)

        for sub, val in subject_data.items():
            st.write(f"{sub} - {val}%")
            st.progress(val / 100)

        # Quick actions
        st.markdown("## 🚀 Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📚 Learning"):
                st.session_state.menu = "Learning"
                st.rerun()

        with col2:
            if st.button("🧠 Quiz"):
                st.session_state.menu = "Quiz"
                st.rerun()

        with col3:
            if st.button("🗺 Map"):
                st.session_state.menu = "Map Practice"
                st.rerun()

    # ---------------- LEARNING ----------------
    elif menu == "Learning":
        learning_ui(user)

    # ---------------- QUIZ ----------------
    elif menu == "Quiz":
        if "selected_path" in st.session_state:
            quiz_ui(user)
        else:
            st.warning("Start quiz from Learning or Daily Challenge")

    # ---------------- MAP ----------------
    elif menu == "Map Practice":
        map_ui()

    # ---------------- DICTIONARY ----------------
    elif menu == "Dictionary":
        dictionary_ui()

    # ---------------- APTITUDE ----------------
    elif menu == "Aptitude":
        aptitude_ui(user)

    # ---------------- REASONING ----------------
    elif menu == "Reasoning":
        reasoning_ui(user)

    # ---------------- ANSWER WRITING ----------------
    elif menu == "Answer Writing":
        answer_writing_ui(user)

    # ---------------- DAILY CHALLENGE ----------------
    elif menu == "Daily Challenge":
        challenge = get_daily_challenge(user, ncert_quiz)

        if challenge:
            sub, cls, ch = challenge

            st.write(sub, cls, ch)

            if st.button("Start Challenge"):

                # RESET QUIZ STATE
                for key in ["q_index", "score", "wrong", "start_time"]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.session_state.selected_path = challenge
                st.session_state.menu = "Quiz"
                st.rerun()

    # ---------------- CURRENT AFFAIRS ----------------
    elif menu == "Current Affairs":
        current_affairs_ui(user)

    # ---------------- LEADERBOARD ----------------
    elif menu == "Leaderboard":
        st.title("🏆 Leaderboard")

        leaderboard = get_leaderboard()

        for i, entry in enumerate(leaderboard[:10]):
            st.write(f"{i+1}. {entry['user']} - {entry['xp']} XP")

        rank = get_user_rank(user)
        st.success(f"Your Rank: {rank}")

    # ---------------- LOGOUT ----------------
    elif menu == "Logout":
        st.session_state.clear()
        st.rerun()


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()