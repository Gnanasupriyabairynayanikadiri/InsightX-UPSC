# =========================================================
# 📁 FILE: core/notifications.py
# SMART NOTIFICATION ENGINE (UPSC OS)
# =========================================================

import streamlit as st
import time
import threading
import uuid

import streamlit.components.v1 as components


# =========================================================
# 🔔 BROWSER NOTIFICATION ENGINE
# =========================================================
def notify(message="Time's up!", title="UPSC OS Alert"):

    """
    Sends browser notification using JS.
    Works in Streamlit (desktop + mobile browsers)
    """

    components.html(
        f"""
        <script>
            function sendNotification() {{
                if (!("Notification" in window)) {{
                    console.log("Browser does not support notifications");
                    return;
                }}

                if (Notification.permission !== "granted") {{
                    Notification.requestPermission();
                }} else {{
                    new Notification("{title}", {{
                        body: "{message}"
                    }});
                }}
            }}

            sendNotification();
        </script>
        """,
        height=0
    )


# =========================================================
# ⏰ SIMPLE TIMER ALERT (NON-BLOCKING)
# =========================================================
def timer_alert(seconds, message="Time completed!"):
    """
    Runs a background timer and triggers notification.
    """

    def run():
        time.sleep(seconds)
        notify(message)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()


# =========================================================
# 🧠 TASK REMINDER SYSTEM
# =========================================================
def schedule_task_reminder(task_name, minutes):

    """
    Schedule a reminder for study task.
    """

    seconds = minutes * 60
    task_id = str(uuid.uuid4())[:8]

    def run():
        time.sleep(seconds)
        notify(
            message=f"Task Complete: {task_name}",
            title="📚 Study Reminder"
        )

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()

    return task_id


# =========================================================
# 🍅 POMODORO NOTIFICATION ENGINE
# =========================================================
def pomodoro_cycle(work_min=25, break_min=5, cycles=4):

    """
    Full Pomodoro system:
    Work → Break → Repeat
    """

    def run():

        for i in range(cycles):

            # WORK SESSION
            notify(
                message=f"Work session {i+1} started",
                title="🔥 Focus Mode ON"
            )

            time.sleep(work_min * 60)

            notify(
                message="Take a short break!",
                title="☕ Break Time"
            )

            time.sleep(break_min * 60)

        notify(
            message="All cycles completed!",
            title="🏆 Pomodoro Done"
        )

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()


# =========================================================
# 📌 SESSION SAFE NOTIFICATION TRACKER
# =========================================================
def session_notify(key, message):

    """
    Prevents duplicate notifications in same session
    """

    if "notifications_sent" not in st.session_state:
        st.session_state.notifications_sent = set()

    if key in st.session_state.notifications_sent:
        return False

    notify(message)
    st.session_state.notifications_sent.add(key)

    return True


# =========================================================
# 🚀 DAILY STUDY REMINDER
# =========================================================
def daily_study_reminder(user="guest"):

    key = f"daily_{user}"

    return session_notify(
        key,
        "Time to start your UPSC study session 📚"
    )


# =========================================================
# 📊 MCQ REMINDER
# =========================================================
def mcq_reminder(user="guest"):

    key = f"mcq_{user}"

    return session_notify(
        key,
        "Practice MCQs now 🧠 for better retention!"
    )


# =========================================================
# 🧾 REVISION ALERT
# =========================================================
def revision_reminder(user="guest"):

    key = f"rev_{user}"

    return session_notify(
        key,
        "Revision time 🔁 Don't skip revision today!"
    )


# =========================================================
# 🔁 SMART AUTO NOTIFIER (HOOK SYSTEM)
# =========================================================
def smart_notify(event_type, user="guest"):

    """
    Central notification router
    """

    if event_type == "study":
        return daily_study_reminder(user)

    elif event_type == "mcq":
        return mcq_reminder(user)

    elif event_type == "revision":
        return revision_reminder(user)

    else:
        return session_notify(
            f"generic_{user}",
            "New update in your UPSC OS 📌"
        )