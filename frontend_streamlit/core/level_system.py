# =========================================================
# 📁 FILE: core/level_system.py
# =========================================================

import os
import json


# =========================================================
# STORAGE
# =========================================================
FILE = "storage/level_progress.json"


# =========================================================
# ENSURE STORAGE
# =========================================================
def ensure_storage():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FILE):

        with open(FILE, "w", encoding="utf-8") as f:

            json.dump({}, f)


# =========================================================
# LOAD DATA
# =========================================================
def load_data():

    ensure_storage()

    try:

        with open(FILE, "r", encoding="utf-8") as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

            return {}

    except:
        return {}


# =========================================================
# SAVE DATA
# =========================================================
def save_data(data):

    ensure_storage()

    with open(FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# GENERATE KEY
# =========================================================
def make_key(subject, chapter, level):

    return f"{subject}_{chapter}_{level}"


# =========================================================
# MARK LEVEL COMPLETION
# =========================================================
def mark_level_completion(

    user,
    subject,
    chapter,
    level

):

    data = load_data()

    if user not in data:
        data[user] = {}

    key = make_key(
        subject,
        chapter,
        level
    )

    current = data[user].get(key, 0)

    data[user][key] = current + 1

    save_data(data)


# =========================================================
# GET LEVEL COUNT
# =========================================================
def get_level_count(

    user,
    subject,
    chapter,
    level

):

    data = load_data()

    if user not in data:
        return 0

    key = make_key(
        subject,
        chapter,
        level
    )

    return data[user].get(key, 0)


# =========================================================
# GET LEVEL PROGRESS
# =========================================================
def get_level_progress(

    user,
    subject,
    chapter

):

    basic = get_level_count(
        user,
        subject,
        chapter,
        "Basic"
    )

    moderate = get_level_count(
        user,
        subject,
        chapter,
        "Moderate"
    )

    advanced = get_level_count(
        user,
        subject,
        chapter,
        "Advanced"
    )

    return {

        "Basic": {

            "completed": basic,

            "required": 3,

            "unlocked": True
        },

        "Moderate": {

            "completed": moderate,

            "required": 3,

            "unlocked": basic >= 3
        },

        "Advanced": {

            "completed": advanced,

            "required": 3,

            "unlocked": moderate >= 3
        }
    }


# =========================================================
# CHECK LEVEL UNLOCK
# =========================================================
def is_level_unlocked(

    user,
    subject,
    chapter,
    level

):

    # =====================================================
    # BASIC ALWAYS OPEN
    # =====================================================
    if level == "Basic":
        return True

    # =====================================================
    # MODERATE
    # =====================================================
    if level == "Moderate":

        basic_done = get_level_count(

            user,
            subject,
            chapter,
            "Basic"
        )

        return basic_done >= 3

    # =====================================================
    # ADVANCED
    # =====================================================
    if level == "Advanced":

        moderate_done = get_level_count(

            user,
            subject,
            chapter,
            "Moderate"
        )

        return moderate_done >= 3

    return False


# =========================================================
# GET NEXT LEVEL
# =========================================================
def get_next_level(level):

    if level == "Basic":
        return "Moderate"

    if level == "Moderate":
        return "Advanced"

    return None


# =========================================================
# GET LEVEL STATUS MESSAGE
# =========================================================
def get_level_status_message(

    user,
    subject,
    chapter,
    level

):

    progress = get_level_progress(

        user,
        subject,
        chapter
    )

    data = progress.get(level, {})

    completed = data.get(
        "completed",
        0
    )

    required = data.get(
        "required",
        3
    )

    unlocked = data.get(
        "unlocked",
        False
    )

    # =====================================================
    # LOCKED
    # =====================================================
    if not unlocked:

        if level == "Moderate":

            remain = max(
                3 -
                progress["Basic"]["completed"],
                0
            )

            return f"""
🔒 Moderate locked

Complete {remain} more
Basic answers with good score
"""

        if level == "Advanced":

            remain = max(
                3 -
                progress["Moderate"]["completed"],
                0
            )

            return f"""
🔒 Advanced locked

Complete {remain} more
Moderate answers with good score
"""

    # =====================================================
    # UNLOCKED
    # =====================================================
    return f"""
🔥 {level} Progress:
{completed}/{required}
"""


# =========================================================
# RESET USER LEVELS
# =========================================================
def reset_user_levels(user):

    data = load_data()

    if user in data:

        data[user] = {}

        save_data(data)


# =========================================================
# GET ALL USER LEVEL DATA
# =========================================================
def get_user_level_data(user):

    data = load_data()

    return data.get(user, {})


# =========================================================
# TOTAL COMPLETED ANSWERS
# =========================================================
def get_total_completed_answers(user):

    user_data = get_user_level_data(user)

    total = 0

    for value in user_data.values():

        total += value

    return total


# =========================================================
# GET USER OVERALL LEVEL
# =========================================================
def get_user_overall_level(user):

    total = get_total_completed_answers(user)

    if total >= 50:
        return "🏆 UPSC Master"

    elif total >= 30:
        return "🔥 Advanced Aspirant"

    elif total >= 15:
        return "📘 Intermediate Aspirant"

    elif total >= 5:
        return "🌱 Beginner Aspirant"

    return "🆕 New Aspirant"