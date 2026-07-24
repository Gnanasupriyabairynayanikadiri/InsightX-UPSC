# =========================================================
# 📁 FILE: core/state_manager.py
# MASTER STABLE VERSION (100% APP.PY COMPATIBLE)
# =========================================================

import streamlit as st


# =========================================================
# 🔧 INIT STATE
# =========================================================
def init_state():

    defaults = {
        "user": None,
        "page": "Home",
        "menu": "Home",
        "selected_subject": None,
        "selected_category": None,
        "selected_chapter": None,
        "selected_topic_index": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# 👤 USER MANAGEMENT
# =========================================================
def get_user():
    return st.session_state.get("user", None)


def set_user(user):
    st.session_state.user = user


# =========================================================
# 🔓 LOGOUT
# =========================================================
def logout_user():

    keys = list(st.session_state.keys())

    for key in keys:
        del st.session_state[key]

    init_state()

    return True


# =========================================================
# 🍔 MENU SYSTEM (CRITICAL FOR APP.PY)
# =========================================================
def set_menu(menu_name):

    if not menu_name:
        menu_name = "Home"

    st.session_state.menu = menu_name
    st.session_state.page = menu_name

    return menu_name


def get_menu():

    return st.session_state.get("menu", "Home")


# =========================================================
# 🧭 NAVIGATION HELPERS (OPTIONAL SUPPORT)
# =========================================================
def navigate(page):

    st.session_state.page = page
    st.session_state.menu = page


def get_page():

    return st.session_state.get("page", "Home")


# =========================================================
# 📌 SAVE LAST STATE (USED IN CORE SUBJECTS UI)
# =========================================================
def save_last_state(subject, category, chapter, topic_index):

    st.session_state.selected_subject = subject
    st.session_state.selected_category = category
    st.session_state.selected_chapter = chapter
    st.session_state.selected_topic_index = topic_index

    return True


# =========================================================
# 📍 FULL STATE SNAPSHOT (DEBUG/ANALYTICS)
# =========================================================
def get_state():

    return {
        "user": st.session_state.get("user"),
        "menu": st.session_state.get("menu"),
        "page": st.session_state.get("page"),
        "subject": st.session_state.get("selected_subject"),
        "category": st.session_state.get("selected_category"),
        "chapter": st.session_state.get("selected_chapter"),
        "topic_index": st.session_state.get("selected_topic_index", 0)
    }