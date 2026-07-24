from datetime import datetime


# ==============================
# 🧹 SAFE GET
# ==============================
def safe_get(data, key, default=None):

    if default is None:
        default = 0

    try:
        return data.get(key, default)
    except Exception:
        return default


# ==============================
# 🎯 MAIN REMINDER ENGINE
# ==============================
def get_reminder_message(user_stats=None, daily_data=None):

    # ==============================
    # 🛡️ SAFE DEFAULTS
    # ==============================
    if user_stats is None:
        user_stats = {}

    if daily_data is None:
        daily_data = {}

    # ==============================
    # 📊 USER DATA
    # ==============================
    xp = safe_get(user_stats, "xp", 0)

    streak = safe_get(user_stats, "streak", 0)

    completed = safe_get(
        daily_data,
        "completed",
        False
    )

    quiz_done = safe_get(
        daily_data,
        "quiz",
        0
    )

    answer_done = safe_get(
        daily_data,
        "answer",
        0
    )

    comment_done = safe_get(
        daily_data,
        "comment",
        0
    )

    # ==============================
    # ⏰ CURRENT TIME
    # ==============================
    hour = datetime.now().hour

    # ==============================
    # 🌅 MORNING REMINDERS
    # ==============================
    if hour < 12:

        if streak >= 7:

            return (
                f"🔥 {streak}-day streak! "
                "Start strong with today's quiz."
            )

        if quiz_done == 0:

            return (
                "🌅 Good morning! "
                "Complete today's quiz to build momentum."
            )

        return (
            "☀️ Nice start today! "
            "Continue your preparation."
        )

    # ==============================
    # 📚 AFTERNOON REMINDERS
    # ==============================
    elif hour < 18:

        if answer_done == 0:

            return (
                "📚 Time for answer writing practice!"
            )

        if comment_done < 2:

            remaining = 2 - comment_done

            return (
                f"💬 Participate in community discussion "
                f"({remaining} more interaction needed)."
            )

        return (
            "🚀 You're progressing well today!"
        )

    # ==============================
    # 🌙 EVENING REMINDERS
    # ==============================
    else:

        if not completed:

            tasks_left = []

            if quiz_done == 0:
                tasks_left.append("Quiz")

            if answer_done == 0:
                tasks_left.append("Answer Writing")

            if comment_done < 2:
                tasks_left.append("Community")

            remaining_tasks = ", ".join(tasks_left)

            return (
                f"🔥 Finish today's mission before midnight!\n\n"
                f"Remaining: {remaining_tasks}"
            )

        # ==============================
        # 🎉 COMPLETED
        # ==============================
        return (
            f"🎉 Excellent work today!\n\n"
            f"⭐ XP: {xp}\n"
            f"🔥 Streak: {streak} days"
        )


# ==============================
# 🎨 REMINDER TYPE
# ==============================
def get_reminder_type(message):

    message = str(message).lower()

    if "🔥" in message:
        return "warning"

    if "🎉" in message:
        return "success"

    if "📚" in message:
        return "info"

    return "normal"


# ==============================
# 📌 REMINDER PRIORITY
# ==============================
def get_reminder_priority(daily_data=None):

    if daily_data is None:
        daily_data = {}

    completed = daily_data.get(
        "completed",
        False
    )

    if completed:
        return "low"

    total = 0

    if daily_data.get("quiz", 0) == 0:
        total += 1

    if daily_data.get("answer", 0) == 0:
        total += 1

    if daily_data.get("comment", 0) < 2:
        total += 1

    if total >= 3:
        return "high"

    if total == 2:
        return "medium"

    return "low"