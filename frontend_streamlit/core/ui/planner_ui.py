# =====================================================
# 📁 FILE: core/ui/planner_ui.py
# SMART UPSC STUDY PLANNER UI
# =====================================================

import streamlit as st

from core.study_os.timetable_generator import (
    get_user_timetable,
    update_user_timetable,
    add_timetable_block,
    delete_timetable_block,
    generate_custom_timetable
)

from core.study_os.revision_engine import (
    get_due_revisions
)

from core.study_os.session_engine import (
    create_session,
    session_controls,
    session_analytics
)

from core.xp import (
    get_xp,
    get_rank,
    get_streak
)


# =====================================================
# SMART TIMETABLE UI
# =====================================================

def smart_timetable_ui(user):

    st.markdown("## 🧠 Smart Timetable (Editable)")

    st.caption(
        "Edit your UPSC study structure dynamically"
    )

    timetable = get_user_timetable(user)

    updated_timetable = []

    # =================================================
    # EXISTING BLOCKS
    # =================================================

    for i, block in enumerate(timetable):

        st.markdown(f"### ⏰ Study Block {i + 1}")

        col1, col2 = st.columns(2)

        with col1:

            start = st.text_input(
                "Start Time",
                value=block.get("start", ""),
                key=f"start_{i}"
            )

        with col2:

            end = st.text_input(
                "End Time",
                value=block.get("end", ""),
                key=f"end_{i}"
            )

        task = st.text_input(
            "Task",
            value=block.get("task", ""),
            key=f"task_{i}"
        )

        updated_timetable.append({

            "start": start,
            "end": end,
            "task": task
        })

        # =============================================
        # SESSION DURATION
        # =============================================

        duration = st.number_input(

            "Session Minutes",

            min_value=5,

            max_value=300,

            value=60,

            key=f"duration_{i}"
        )

        col_a, col_b = st.columns(2)

        # =============================================
        # START SESSION
        # =============================================

        with col_a:

            if st.button(
                f"▶ Start Session {i+1}",
                key=f"session_{i}"
            ):

                session_id = create_session(

                    user=user,

                    session_name=task,

                    duration_minutes=duration,

                    subject="UPSC",

                    mode="Study"
                )

                st.session_state[
                    f"active_session_{i}"
                ] = session_id

                st.success(
                    f"Started session for {task}"
                )

                st.rerun()

        # =============================================
        # DELETE BLOCK
        # =============================================

        with col_b:

            if st.button(
                f"🗑 Delete Block {i+1}",
                key=f"delete_{i}"
            ):

                delete_timetable_block(
                    user,
                    i
                )

                st.warning("Block deleted!")

                st.rerun()

        # =============================================
        # SHOW TIMER
        # =============================================

        session_key = f"active_session_{i}"

        if session_key in st.session_state:

            session_controls(
                user,
                st.session_state[session_key]
            )

        st.markdown("---")

    # =================================================
    # ADD NEW BLOCK
    # =================================================

    st.markdown("## ➕ Add New Study Block")

    col1, col2, col3 = st.columns(3)

    with col1:

        new_start = st.text_input(
            "Start Time",
            key="new_start"
        )

    with col2:

        new_end = st.text_input(
            "End Time",
            key="new_end"
        )

    with col3:

        new_task = st.text_input(
            "Task",
            key="new_task"
        )

    if st.button("➕ Add Block"):

        if new_start and new_end and new_task:

            add_timetable_block(

                user=user,

                start=new_start,

                end=new_end,

                task=new_task
            )

            st.success(
                "New study block added!"
            )

            st.rerun()

        else:

            st.error(
                "Please fill all fields"
            )

    # =================================================
    # SAVE TIMETABLE
    # =================================================

    st.markdown("---")

    if st.button("💾 Save Timetable"):

        update_user_timetable(
            user,
            updated_timetable
        )

        st.success(
            "Timetable saved successfully!"
        )

    # =================================================
    # FINAL VIEW
    # =================================================

    st.markdown("---")

    st.markdown("## 📊 Current Timetable View")

    for block in updated_timetable:

        st.success(

            f"🕒 {block['start']} - "
            f"{block['end']} → "
            f"{block['task']}"
        )


# =====================================================
# CUSTOM TIMETABLE UI
# =====================================================

def custom_timetable_ui(user):

    st.markdown("## 📖 Build Your Own Timetable")

    if "custom_plan" not in st.session_state:
        st.session_state.custom_plan = []

    timetable = st.session_state.custom_plan

    if len(timetable) == 0:
        st.info(
            "No study blocks yet. Add your own timetable below."
        )

    # =================================================
    # EDITABLE BLOCKS
    # =================================================

    for i, block in enumerate(timetable):

        st.markdown(f"### ⏰ Study Block {i+1}")

        col1, col2 = st.columns(2)

        with col1:

            start = st.text_input(

                "Start Time",

                value=block["start"],

                key=f"custom_start_{i}"
            )

        with col2:

            end = st.text_input(

                "End Time",

                value=block["end"],

                key=f"custom_end_{i}"
            )

        task = st.text_input(

            "Task",

            value=block["task"],

            key=f"custom_task_{i}"
        )

        updated_plan.append({

            "start": start,

            "end": end,

            "task": task
        })

        # =============================================
        # TIMER
        # =============================================

        duration = st.number_input(

            "Session Minutes",

            min_value=5,

            max_value=300,

            value=60,

            key=f"custom_duration_{i}"
        )

        if st.button(
            f"▶ Start Study Session {i+1}",
            key=f"custom_session_{i}"
        ):

            session_id = create_session(

                user=user,

                session_name=task,

                duration_minutes=duration,

                subject="UPSC",

                mode="Study"
            )

            st.session_state[
                f"custom_active_session_{i}"
            ] = session_id

            st.rerun()

        session_key = f"custom_active_session_{i}"

        if session_key in st.session_state:

            session_controls(

                user,

                st.session_state[session_key]
            )

        st.markdown("---")

    # =================================================
    # ADD CUSTOM BLOCK
    # =================================================

    st.markdown("## ➕ Add Extra Study Block")

    c1, c2, c3 = st.columns(3)

    with c1:

        extra_start = st.text_input(
            "New Start",
            key="extra_start"
        )

    with c2:

        extra_end = st.text_input(
            "New End",
            key="extra_end"
        )

    with c3:

        extra_task = st.text_input(
            "New Task",
            key="extra_task"
        )

    if st.button("➕ Add Extra Block"):

        if extra_start and extra_end and extra_task:

            st.session_state.custom_plan.append({

                "start": extra_start,

                "end": extra_end,

                "task": extra_task
            })

            st.success("Study block added!")

            st.rerun()

    # =================================================
    # FINAL VIEW
    # =================================================

    st.markdown("## 📊 Final Timetable")

    for block in st.session_state.custom_plan:

        st.success(

            f"🕒 {block['start']} - "
            f"{block['end']} → "
            f"{block['task']}"
        )


# =====================================================
# POMODORO MODE
# =====================================================

def pomodoro_ui(user):

    st.markdown("## 🍅 Pomodoro Study Mode")

    study_minutes = st.number_input(

        "Study Minutes",

        min_value=15,

        max_value=90,

        value=25
    )

    break_minutes = st.number_input(

        "Break Minutes",

        min_value=1,

        max_value=30,

        value=5
    )

    cycles = st.number_input(

        "Cycles",

        min_value=1,

        max_value=10,

        value=4
    )

    st.success(

        f"{cycles} cycles of "
        f"{study_minutes} mins study "
        f"+ {break_minutes} mins break"
    )

    if st.button("▶ Start Pomodoro"):

        session_id = create_session(

            user=user,

            session_name="Pomodoro Session",

            duration_minutes=study_minutes,

            subject="UPSC",

            mode="Pomodoro"
        )

        st.session_state[
            "pomodoro_session"
        ] = session_id

    if "pomodoro_session" in st.session_state:

        session_controls(

            user,

            st.session_state[
                "pomodoro_session"
            ]
        )


# =====================================================
# DEEP WORK MODE
# =====================================================

def deep_work_ui(user):

    st.markdown("## 🎯 Deep Work Mode")

    hours = st.slider(

        "Deep Work Hours",

        1,
        8,
        3
    )

    st.info(

        f"Focused UPSC study for "
        f"{hours} hour(s)"
    )

    if st.button("▶ Start Deep Work"):

        session_id = create_session(

            user=user,

            session_name="Deep Work Session",

            duration_minutes=hours * 60,

            subject="UPSC",

            mode="Deep Work"
        )

        st.session_state[
            "deep_work_session"
        ] = session_id

    if "deep_work_session" in st.session_state:

        session_controls(

            user,

            st.session_state[
                "deep_work_session"
            ]
        )


# =====================================================
# REVISION UI
# =====================================================

def revision_ui(user):

    st.markdown("## 🔁 Due Revisions")

    revisions = get_due_revisions(user)

    if not revisions:

        st.success(
            "No revisions due today"
        )

    else:

        for item in revisions:

            st.write(f"📘 {item}")


# =====================================================
# ANALYTICS UI
# =====================================================

def analytics_ui(user):

    st.markdown("## 📊 Study Analytics")

    analytics = session_analytics(user)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "📚 Sessions",

            analytics["total_sessions"]
        )

    with col2:

        st.metric(

            "⏳ Study Minutes",

            analytics["total_minutes"]
        )

    with col3:

        st.metric(

            "⭐ XP Earned",

            analytics["total_xp"]
        )


# =====================================================
# MAIN UI
# =====================================================

def planner_ui(
    user="guest",
    goal="IAS"
):

    st.title("📅 Smart UPSC Study Planner")

    # =================================================
    # DASHBOARD
    # =================================================

    st.markdown("## 📊 Performance Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🔥 Streak",
            get_streak(user)
        )

    with col2:

        st.metric(
            "⭐ XP",
            get_xp(user)
        )

    with col3:

        st.metric(
            "🏆 Rank",
            get_rank(user)
        )

    st.markdown("---")

    # =================================================
    # STUDY MODES
    # =================================================

    study_mode = st.selectbox(

        "🧠 Select Study Mode",

        [

            "Smart Study Planner",

            "Custom Timetable",

            "Pomodoro Mode",

            "Deep Work Mode",

            "Revision Mode",

            "Analytics"
        ]
    )

    # =================================================
    # ROUTING
    # =================================================

    if study_mode == "Smart Study Planner":

        smart_timetable_ui(user)

    elif study_mode == "Custom Timetable":

        custom_timetable_ui(user)

    elif study_mode == "Pomodoro Mode":

        pomodoro_ui(user)

    elif study_mode == "Deep Work Mode":

        deep_work_ui(user)

    elif study_mode == "Revision Mode":

        revision_ui(user)

    elif study_mode == "Analytics":

        analytics_ui(user)


# =====================================================
# ENTRY
# =====================================================

def run(user="guest"):

    planner_ui(user)