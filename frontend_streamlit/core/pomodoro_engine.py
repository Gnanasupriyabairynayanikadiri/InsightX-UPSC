# =====================================================
# 📁 FILE: core/pomodoro_engine.py
# UPSC POMODORO ENGINE (STREAMLIT SAFE)
# =====================================================

import streamlit as st
import time
import streamlit.components.v1 as components


# =====================================================
# 🔔 NOTIFICATION (BROWSER ALERT)
# =====================================================
def notify(message="Time's up! 🍅"):

    components.html(f"""
    <script>
        if (Notification.permission !== "granted") {{
            Notification.requestPermission();
        }}

        if (Notification.permission === "granted") {{
            new Notification("{message}");
        }}
    </script>
    """, height=0)


# =====================================================
# DEFAULT SETTINGS
# =====================================================
DEFAULT_WORK = 25 * 60
DEFAULT_BREAK = 5 * 60


# =====================================================
# INIT STATE
# =====================================================
def init_pomodoro():

    if "pomo_mode" not in st.session_state:
        st.session_state.pomo_mode = "work"   # work / break

    if "pomo_running" not in st.session_state:
        st.session_state.pomo_running = False

    if "pomo_time" not in st.session_state:
        st.session_state.pomo_time = DEFAULT_WORK

    if "pomo_cycle" not in st.session_state:
        st.session_state.pomo_cycle = 1

    if "work_duration" not in st.session_state:
        st.session_state.work_duration = DEFAULT_WORK

    if "break_duration" not in st.session_state:
        st.session_state.break_duration = DEFAULT_BREAK


# =====================================================
# SWITCH MODE
# =====================================================
def switch_mode():

    if st.session_state.pomo_mode == "work":
        st.session_state.pomo_mode = "break"
        st.session_state.pomo_time = st.session_state.break_duration
        notify("Break time! ☕")

    else:
        st.session_state.pomo_mode = "work"
        st.session_state.pomo_time = st.session_state.work_duration
        st.session_state.pomo_cycle += 1
        notify("Back to study! 📚")


# =====================================================
# FORMAT TIMER
# =====================================================
def format_time(seconds):

    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


# =====================================================
# MAIN POMODORO UI
# =====================================================
def pomodoro_ui():

    init_pomodoro()

    st.title("🍅 UPSC Pomodoro Engine")

    # =================================================
    # SETTINGS
    # =================================================
    st.markdown("### ⚙️ Settings")

    col1, col2 = st.columns(2)

    with col1:
        work_min = st.number_input("Work (min)", 5, 120, 25)
    with col2:
        break_min = st.number_input("Break (min)", 1, 30, 5)

    st.session_state.work_duration = work_min * 60
    st.session_state.break_duration = break_min * 60

    # =================================================
    # DISPLAY STATUS
    # =================================================
    mode = st.session_state.pomo_mode.upper()

    st.markdown(f"## {mode} SESSION")
    st.markdown(f"### ⏱ {format_time(st.session_state.pomo_time)}")

    st.progress(
        st.session_state.pomo_time /
        (st.session_state.work_duration
         if st.session_state.pomo_mode == "work"
         else st.session_state.break_duration)
    )

    st.markdown(f"📊 Cycle: {st.session_state.pomo_cycle}")

    # =================================================
    # CONTROLS
    # =================================================
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶ Start"):
            st.session_state.pomo_running = True

    with col2:
        if st.button("⏸ Pause"):
            st.session_state.pomo_running = False

    with col3:
        if st.button("🔄 Reset"):
            st.session_state.pomo_running = False
            st.session_state.pomo_mode = "work"
            st.session_state.pomo_time = st.session_state.work_duration
            st.session_state.pomo_cycle = 1

    # =================================================
    # TIMER ENGINE (STREAMLIT SIMULATION LOOP)
    # =================================================
    if st.session_state.pomo_running:

        if st.session_state.pomo_time > 0:
            st.session_state.pomo_time -= 1
            time.sleep(1)
            st.rerun()

        else:
            switch_mode()
            st.rerun()

    # =================================================
    # UPSC BOOST TIPS
    # =================================================
    st.markdown("---")
    st.markdown("### 📚 UPSC Focus Tips")

    tips = [
        "📖 Use Pomodoro for NCERT + Revision",
        "🧠 Revise after every 2 cycles",
        "✍️ Use break time for light current affairs",
        "🚫 Avoid phone during work session",
        "🔁 4 Pomodoros = 1 deep study block"
    ]

    for t in tips:
        st.write("•", t)