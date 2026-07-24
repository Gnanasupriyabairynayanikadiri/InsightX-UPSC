# =========================================================
# 📁 FILE: core/study_os/session_engine.py
# UNIVERSAL UPSC SESSION ENGINE
# LIVE TIMER + PAUSE + RESUME + XP + ANALYTICS
# =========================================================

import os
import json
import time

from datetime import datetime

import streamlit as st

from streamlit_autorefresh import st_autorefresh


# =========================================================
# STORAGE
# =========================================================

SESSION_FILE = "storage/session_data.json"


# =========================================================
# ENSURE STORAGE
# =========================================================

def ensure_storage():

    os.makedirs(
        "storage",
        exist_ok=True
    )

    if not os.path.exists(SESSION_FILE):

        with open(
            SESSION_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump({}, f)


# =========================================================
# LOAD SESSIONS
# =========================================================

def load_sessions():

    ensure_storage()

    try:

        with open(
            SESSION_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

            return {}

    except:
        return {}


# =========================================================
# SAVE SESSIONS
# =========================================================

def save_sessions(data):

    ensure_storage()

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# NORMALIZE USER
# =========================================================

def normalize_user(user):

    if not user:
        return "guest"

    return str(user).strip().lower()


# =========================================================
# CREATE SESSION
# =========================================================

def create_session(
    user,
    session_name,
    duration_minutes,
    subject="General",
    mode="Study"
):

    user = normalize_user(user)

    data = load_sessions()

    if user not in data:
        data[user] = {}

    session_id = str(
        int(time.time() * 1000)
    )

    data[user][session_id] = {

        "session_name": session_name,

        "subject": subject,

        "mode": mode,

        "duration_minutes": int(duration_minutes),

        "remaining_seconds": int(duration_minutes) * 60,

        "started": False,

        "paused": False,

        "completed": False,

        "start_timestamp": None,

        "created_at": str(datetime.now()),

        "completed_at": None,

        "xp_earned": 0
    }

    save_sessions(data)

    return session_id


# =========================================================
# GET SESSION
# =========================================================

def get_session(user, session_id):

    user = normalize_user(user)

    data = load_sessions()

    return data.get(user, {}).get(session_id)


# =========================================================
# UPDATE SESSION
# =========================================================

def update_session(
    user,
    session_id,
    session_data
):

    user = normalize_user(user)

    data = load_sessions()

    if user not in data:
        data[user] = {}

    data[user][session_id] = session_data

    save_sessions(data)


# =========================================================
# CALCULATE XP
# =========================================================

def calculate_xp(session):

    duration = session.get(
        "duration_minutes",
        0
    )

    mode = session.get(
        "mode",
        "Study"
    )

    xp = duration // 5

    if mode == "Pomodoro":

        xp += 10

    elif mode == "Deep Work":

        xp += 25

    elif mode == "Mock Test":

        xp += 50

    return int(xp)


# =========================================================
# COMPLETE SESSION
# =========================================================

def complete_session(user, session_id):

    session = get_session(
        user,
        session_id
    )

    if not session:
        return 0

    if session.get("completed"):
        return session.get("xp_earned", 0)

    session["completed"] = True

    session["paused"] = False

    session["remaining_seconds"] = 0

    session["completed_at"] = str(datetime.now())

    xp = calculate_xp(session)

    session["xp_earned"] = xp

    update_session(
        user,
        session_id,
        session
    )

    return xp


# =========================================================
# FORMAT TIME
# =========================================================

def format_time(seconds):

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    secs = seconds % 60

    if hours > 0:

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    return f"{minutes:02d}:{secs:02d}"


# =========================================================
# UNIVERSAL LIVE TIMER
# =========================================================

def live_timer(
    session_key,
    duration_minutes
):

    # =====================================================
    # AUTO REFRESH EVERY SECOND
    # =====================================================

    st_autorefresh(
        interval=1000,
        key=f"refresh_{session_key}"
    )

    started_key = f"{session_key}_started"

    start_time_key = f"{session_key}_start_time"

    paused_key = f"{session_key}_paused"

    remaining_key = f"{session_key}_remaining"

    completed_key = f"{session_key}_completed"

    # =====================================================
    # INITIALIZE
    # =====================================================

    if started_key not in st.session_state:

        st.session_state[started_key] = False

    if start_time_key not in st.session_state:

        st.session_state[start_time_key] = None

    if paused_key not in st.session_state:

        st.session_state[paused_key] = False

    if remaining_key not in st.session_state:

        st.session_state[remaining_key] = (
            duration_minutes * 60
        )

    if completed_key not in st.session_state:

        st.session_state[completed_key] = False

    # =====================================================
    # BUTTONS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # START / RESUME
    # =====================================================

    with col1:

        if (
            not st.session_state[started_key]
            or st.session_state[paused_key]
        ):

            label = (
                "🔄 Resume"
                if st.session_state[paused_key]
                else "▶ Start"
            )

            if st.button(
                label,
                key=f"start_btn_{session_key}"
            ):

                st.session_state[started_key] = True

                st.session_state[paused_key] = False

                elapsed_before_pause = (

                    duration_minutes * 60
                    -
                    st.session_state[remaining_key]
                )

                st.session_state[start_time_key] = (

                    time.time()
                    -
                    elapsed_before_pause
                )

                st.rerun()

    # =====================================================
    # PAUSE
    # =====================================================

    with col2:

        if (
            st.session_state[started_key]
            and
            not st.session_state[paused_key]
            and
            not st.session_state[completed_key]
        ):

            if st.button(
                "⏸ Pause",
                key=f"pause_btn_{session_key}"
            ):

                elapsed = int(
                    time.time()
                    -
                    st.session_state[start_time_key]
                )

                remaining = max(
                    duration_minutes * 60
                    -
                    elapsed,
                    0
                )

                st.session_state[remaining_key] = remaining

                st.session_state[paused_key] = True

                st.rerun()

    # =====================================================
    # COMPLETE
    # =====================================================

    with col3:

        if st.button(
            "✅ Complete",
            key=f"complete_btn_{session_key}"
        ):

            st.session_state[completed_key] = True

            st.success("🏆 Session Completed!")

            st.balloons()

            return True

    # =====================================================
    # TIMER LOGIC
    # =====================================================

    if (
        st.session_state[started_key]
        and
        not st.session_state[paused_key]
        and
        not st.session_state[completed_key]
    ):

        elapsed = int(
            time.time()
            -
            st.session_state[start_time_key]
        )

        remaining = max(
            duration_minutes * 60
            -
            elapsed,
            0
        )

        st.session_state[remaining_key] = remaining

    else:

        remaining = st.session_state[remaining_key]

    # =====================================================
    # DISPLAY TIMER
    # =====================================================

    st.markdown(
        f"""
        ## ⏳ {remaining//60:02d}:{remaining%60:02d}
        """
    )

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    progress = (
        (
            duration_minutes * 60
            -
            remaining
        )
        /
        (duration_minutes * 60)
    )

    st.progress(
        max(0.0, min(progress, 1.0))
    )

    # =====================================================
    # TIME UP
    # =====================================================

    if remaining == 0:

        st.session_state[completed_key] = True

        st.error("⏰ Time Up!")

        st.balloons()

        return True

    return False


# =========================================================
# SESSION UI CONTROLS
# =========================================================

def session_controls(user, session_id):

    session = get_session(
        user,
        session_id
    )

    if not session:

        st.error("Session not found")

        return

    st.markdown(

        f"""
        ### 📚 {session['session_name']}
        """
    )

    finished = live_timer(

        session_key=session_id,

        duration_minutes=session["duration_minutes"]
    )

    if finished:

        xp = complete_session(
            user,
            session_id
        )

        st.success(
            f"🏆 Session Completed +{xp} XP"
        )


# =========================================================
# GET USER SESSIONS
# =========================================================

def get_user_sessions(user):

    user = normalize_user(user)

    data = load_sessions()

    return data.get(user, {})


# =========================================================
# TOTAL STUDY MINUTES
# =========================================================

def total_study_minutes(user):

    sessions = get_user_sessions(user)

    total = 0

    for session in sessions.values():

        if session.get("completed"):

            total += session.get(
                "duration_minutes",
                0
            )

    return total


# =========================================================
# TOTAL XP
# =========================================================

def total_xp(user):

    sessions = get_user_sessions(user)

    xp = 0

    for session in sessions.values():

        xp += session.get(
            "xp_earned",
            0
        )

    return xp


# =========================================================
# SESSION ANALYTICS
# =========================================================

def session_analytics(user):

    sessions = get_user_sessions(user)

    total_sessions = len(sessions)

    completed_sessions = sum(

        1 for s in sessions.values()

        if s.get("completed")
    )

    deep_work_sessions = sum(

        1 for s in sessions.values()

        if s.get("mode") == "Deep Work"
    )

    pomodoro_sessions = sum(

        1 for s in sessions.values()

        if s.get("mode") == "Pomodoro"
    )

    return {

        "total_sessions": total_sessions,

        "completed_sessions": completed_sessions,

        "deep_work_sessions": deep_work_sessions,

        "pomodoro_sessions": pomodoro_sessions,

        "total_minutes": total_study_minutes(user),

        "total_xp": total_xp(user)
    }