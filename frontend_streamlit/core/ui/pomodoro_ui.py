# =========================================================
# 📁 FILE: core/pomodoro_ui.py
# UPSC POMODORO ENGINE (STREAMLIT READY)
# =========================================================

import streamlit as st
import time

from core.notifications import notify


# =========================================================
# DEFAULT SETTINGS
# =========================================================
DEFAULT_WORK_MIN = 25
DEFAULT_BREAK_MIN = 5


# =========================================================
# INIT STATE
# =========================================================
def init_pomodoro_state():

    if "pomodoro_mode" not in st.session_state:
        st.session_state.pomodoro_mode = "work"

    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False

    if "pomodoro_seconds" not in st.session_state:
        st.session_state.pomodoro_seconds = DEFAULT_WORK_MIN * 60

    if "pomodoro_cycle" not in st.session_state:
        st.session_state.pomodoro_cycle = 1


# =========================================================
# RESET TIMER
# =========================================================
def reset_timer(mode="work"):

    if mode == "work":
        st.session_state.pomodoro_seconds = DEFAULT_WORK_MIN * 60
        st.session_state.pomodoro_mode = "work"

    else:
        st.session_state.pomodoro_seconds = DEFAULT_BREAK_MIN * 60
        st.session_state.pomodoro_mode = "break"


# =========================================================
# FORMAT TIME
# =========================================================
def format_time(seconds):

    minutes = seconds // 60
    sec = seconds % 60

    return f"{minutes:02d}:{sec:02d}"


# =========================================================
# AUTO SWITCH LOGIC
# =========================================================
def switch_mode():

    if st.session_state.pomodoro_mode == "work":

        st.session_state.pomodoro_mode = "break"
        st.session_state.pomodoro_cycle += 1

        reset_timer("break")

        notify("Break time 🍵", "UPSC Pomodoro")

    else:

        st.session_state.pomodoro_mode = "work"

        reset_timer("work")

        notify("Focus time 🍅", "UPSC Pomodoro")


# =========================================================
# TIMER TICK
# =========================================================
def tick():

    if st.session_state.pomodoro_running:

        if st.session_state.pomodoro_seconds > 0:

            st.session_state.pomodoro_seconds -= 1

        else:

            switch_mode()


# =========================================================
# MAIN UI
# =========================================================
def pomodoro_ui():

    init_pomodoro_state()

    st.title("🍅 UPSC Pomodoro Engine")

    st.caption("Focus system designed for deep UPSC study sessions")

    # =====================================================
    # STATUS
    # =====================================================
    mode = st.session_state.pomodoro_mode
    seconds = st.session_state.pomodoro_seconds

    st.markdown(f"## 🎯 Mode: {mode.upper()}")

    st.markdown(f"### ⏱️ {format_time(seconds)}")

    st.progress(
        seconds / (DEFAULT_WORK_MIN * 60)
        if mode == "work"
        else seconds / (DEFAULT_BREAK_MIN * 60)
    )

    st.markdown("---")

    # =====================================================
    # CONTROL BUTTONS
    # =====================================================
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶ Start"):

            st.session_state.pomodoro_running = True

    with col2:
        if st.button("⏸ Pause"):

            st.session_state.pomodoro_running = False

    with col3:
        if st.button("🔄 Reset"):

            st.session_state.pomodoro_running = False

            reset_timer(mode)

    # =====================================================
    # MANUAL TICK (Streamlit refresh based)
    # =====================================================
    tick()

    st.markdown("---")

    # =====================================================
    # SESSION INFO
    # =====================================================
    st.markdown("## 📊 Session Stats")

    st.write(f"🍅 Completed Cycles: {st.session_state.pomodoro_cycle - 1}")

    if mode == "work":

        st.info("📚 Focus Mode Active — Avoid distractions")

    else:

        st.success("☕ Break Mode — Relax your mind")

    # =====================================================
    # UPSC TIPS
    # =====================================================
    st.markdown("---")

    st.markdown("## 🧠 UPSC Pomodoro Tips")

    tips = [

        "Study NCERT during work sessions",

        "Use break time for revision only",

        "Do MCQs after 2–3 cycles",

        "Avoid switching subjects in same session",

        "Track weak areas after each cycle"
    ]

    for tip in tips:

        st.write(f"• {tip}")