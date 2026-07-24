# ==========================================
# 📁 FILE: frontend_streamlit/app.py
# FINAL CLEAN STABLE VERSION (PRODUCTION READY)
# ==========================================

import streamlit as st
import json
import os

# ==========================================
# CORE MODULES
# ==========================================

from core.learning import learning_ui

from core.quiz_engine import (
    quiz_ui,
    reset_quiz
)

from core.current_affairs.ui import current_affairs_ui
from core.answer_engine.answer_ui import answer_ui
from core.map_ui import map_ui

from core.ui.planner_ui import run as study_planner_ui

from core.dictionary import dictionary_ui
from core.community_ui import community_ui
from core.progress_dashboard import progress_dashboard_ui
from core.core_subjects_ui import core_subjects_ui
from core.bookmarks_ui import bookmarks_ui
from core.pyq_ui import pyq_ui

# ==========================================
# STATE MANAGER
# ==========================================

from core.state_manager import (
    init_state,
    set_user,
    get_user,
    logout_user,
    set_menu,
    get_menu
)

# ==========================================
# XP SYSTEM
# ==========================================

from core.xp import (
    get_xp,
    get_level,
    get_streak,
    update_streak,
    get_leaderboard,
    get_rank
)

# ==========================================
# STORAGE
# ==========================================

USERS_FILE = "storage/users.json"


# ==========================================
# USER DATA HELPERS
# ==========================================

def load_users():
    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(data):
    os.makedirs("storage", exist_ok=True)

    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==========================================
# REGISTER UI
# ==========================================

def register_ui():

    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    goal = st.selectbox("🎯 Goal", ["IAS", "IPS", "IFS", "IRS"])

    if st.button("Register"):

        if not username or not password:
            st.error("Please fill all fields")
            return

        users = load_users()

        if username in users:
            st.error("User already exists")
            return

        users[username] = {
            "password": password,
            "goal": goal,
            "xp": 0,
            "streak": 0,
            "completed_chapters": [],
            "completed_quizzes": []
        }

        save_users(users)

        st.success("✅ Registered successfully")


# ==========================================
# LOGIN UI
# ==========================================

def login_ui():

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        users = load_users()

        user_data = users.get(username)

        if user_data and user_data["password"] == password:

            set_user(username)
            update_streak(username)
            reset_quiz()

            set_menu("Home")

            st.rerun()

        else:
            st.error("❌ Invalid credentials")


# ==========================================
# SIDEBAR
# ==========================================

def sidebar_ui(user):

    users = load_users()
    user_data = users.get(user, {})

    st.sidebar.title("🚀 InsightX")

    st.sidebar.markdown(f"""
### 👤 {user}

🎯 Goal: {user_data.get("goal", "IAS")}

⭐ XP: {get_xp(user)}

🏆 Level: {get_level(get_xp(user))}

🔥 Streak: {get_streak(user)}
""")

    menu_options = [
        "Home",
        "Learning",
        "Quiz",
        "Core Subjects",
        "PYQ",
        "Bookmarks",
        "Answer Writing",
        "Current Affairs",
        "Map Practice",
        "Study Planner",
        "Dictionary",
        "Community",
        "Progress Dashboard",
        "Leaderboard",
        "Logout"
    ]

    current_menu = get_menu()

    return st.sidebar.radio(
        "📚 Navigation",
        menu_options,
        index=menu_options.index(current_menu)
        if current_menu in menu_options else 0
    )


# ==========================================
# HOME
# ==========================================

def home_ui(user):

    st.title("🏠 Home")
    st.success(f"Welcome back {user}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📖 Learning"):
            set_menu("Learning")
            st.rerun()

    with col2:
        if st.button("🧠 Quiz"):
            set_menu("Quiz")
            st.rerun()

    with col3:
        if st.button("📚 Core Subjects"):
            set_menu("Core Subjects")
            st.rerun()


# ==========================================
# LEADERBOARD
# ==========================================

def leaderboard_ui(user):

    st.title("🏆 Leaderboard")

    leaderboard = get_leaderboard()

    for i, u in enumerate(leaderboard, 1):
        st.write(f"{i}. {u['user']} — {u['xp']} XP")

    st.success(f"Your Rank: #{get_rank(user)}")


# ==========================================
# ROUTER
# ==========================================

def route(menu, user):

    routes = {
        "Home": home_ui,
        "Learning": learning_ui,
        "Quiz": quiz_ui,
        "Core Subjects": core_subjects_ui,
        "PYQ": pyq_ui,
        "Bookmarks": bookmarks_ui,
        "Answer Writing": answer_ui,
        "Current Affairs": current_affairs_ui,
        "Map Practice": map_ui,
        "Dictionary": dictionary_ui,
        "Community": community_ui,
        "Progress Dashboard": progress_dashboard_ui,
        "Leaderboard": leaderboard_ui,
    }

    if menu == "Study Planner":
        users = load_users()
        study_planner_ui(user)
        return

    if menu == "Logout":
        logout_user()
        reset_quiz()
        set_menu("Home")
        st.rerun()
        return

    handler = routes.get(menu)

    if handler:
        handler(user)
    else:
        st.warning("Unknown section")


# ==========================================
# MAIN APP
# ==========================================

def main():

    st.set_page_config(
        page_title="InsightX",
        page_icon="🚀",
        layout="wide"
    )

    init_state()

    user = get_user()

    if not user:

        st.title("🚀 InsightX")

        choice = st.radio(
            "Select",
            ["Login", "Register"],
            horizontal=True
        )

        if choice == "Login":
            login_ui()
        else:
            register_ui()

        return

    menu = sidebar_ui(user)
    set_menu(menu)

    try:
        route(menu, user)

    except Exception as e:
        st.error(f"App Error: {e}")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()