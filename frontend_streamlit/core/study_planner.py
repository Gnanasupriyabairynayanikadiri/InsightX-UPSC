# =====================================================
# 📁 FILE: core/study_planner.py
# UPSC STUDY PLANNER ROUTER
# SMART PLANNER + CUSTOM TIMETABLE + POMODORO
# =====================================================

from core.ui.planner_ui import (
    planner_ui
)


# =====================================================
# MAIN STUDY PLANNER
# =====================================================

def study_planner_ui(
    user="guest",
    goal="IAS"
):

    planner_ui(

        user=user,

        goal=goal
    )


# =====================================================
# RUN ENTRY
# =====================================================

def run(
    user="guest",
    goal="IAS"
):

    study_planner_ui(

        user=user,

        goal=goal
    )


# =====================================================
# DIRECT EXECUTION SUPPORT
# =====================================================

if __name__ == "__main__":

    run()