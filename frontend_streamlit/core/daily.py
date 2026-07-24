# core/daily.py

import json
import os
import random

from datetime import date

# ==============================
# FILE
# ==============================
FILE = "storage/daily.json"


# ==============================
# LOAD DATA
# ==============================
def load_daily():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except Exception:
        return {}


# ==============================
# SAVE DATA
# ==============================
def save_daily(data):

    os.makedirs("storage", exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# TODAY
# ==============================
def get_today():

    return str(date.today())


# ==============================
# DAILY QUESTIONS
# ==============================
daily_questions = [

    {
        "subject": "Geography",
        "level": "Basic",

        "question":
        "Which river is the longest in India?",

        "options":
        ["Ganga", "Godavari", "Krishna", "Yamuna"],

        "answer":
        "Ganga",

        "explanation":
        "Ganga is considered the longest river in India with major cultural and economic importance."
    },

    {
        "subject": "Geography",
        "level": "Basic",

        "question":
        "Which state has the longest coastline in India?",

        "options":
        ["Tamil Nadu", "Gujarat", "Andhra Pradesh", "Kerala"],

        "answer":
        "Gujarat",

        "explanation":
        "Gujarat has the longest coastline in India extending over 1600 km."
    },

    {
        "subject": "Polity",
        "level": "Basic",

        "question":
        "Who is known as the Father of the Indian Constitution?",

        "options":
        [
            "Jawaharlal Nehru",
            "B. R. Ambedkar",
            "Rajendra Prasad",
            "Sardar Patel"
        ],

        "answer":
        "B. R. Ambedkar",

        "explanation":
        "Dr. B. R. Ambedkar was the chairman of the Drafting Committee of the Constitution."
    },

    {
        "subject": "History",
        "level": "Moderate",

        "question":
        "The Permanent Settlement system was introduced by whom?",

        "options":
        [
            "Lord Cornwallis",
            "Lord Curzon",
            "Lord Ripon",
            "Lord Dalhousie"
        ],

        "answer":
        "Lord Cornwallis",

        "explanation":
        "Permanent Settlement was introduced in Bengal in 1793 by Lord Cornwallis."
    },

    {
        "subject": "Economy",
        "level": "Moderate",

        "question":
        "Which institution releases the World Economic Outlook report?",

        "options":
        [
            "World Bank",
            "IMF",
            "WTO",
            "ADB"
        ],

        "answer":
        "IMF",

        "explanation":
        "International Monetary Fund publishes the World Economic Outlook report."
    },

    {
        "subject": "Environment",
        "level": "Advanced",

        "question":
        "Which gas contributes the most to global warming?",

        "options":
        [
            "Oxygen",
            "Carbon Dioxide",
            "Nitrogen",
            "Hydrogen"
        ],

        "answer":
        "Carbon Dioxide",

        "explanation":
        "Carbon dioxide is the major greenhouse gas contributing to global warming."
    }
]


# ==============================
# GET TODAY QUESTION
# ==============================
def get_today_question():

    data = load_daily()

    today = get_today()

    # --------------------------
    # INIT DAY
    # --------------------------
    if today not in data:

        data[today] = {
            "question": {},
            "users": {}
        }

    # --------------------------
    # GENERATE DAILY QUESTION
    # --------------------------
    if not data[today].get("question"):

        selected = random.choice(daily_questions)

        data[today]["question"] = selected

        save_daily(data)

    return data[today]["question"]


# ==============================
# INIT USER DAILY
# ==============================
def init_user_daily(user):

    data = load_daily()

    today = get_today()

    # --------------------------
    # INIT TODAY
    # --------------------------
    if today not in data:

        data[today] = {
            "question": {},
            "users": {}
        }

    # --------------------------
    # INIT USERS
    # --------------------------
    if "users" not in data[today]:

        data[today]["users"] = {}

    # --------------------------
    # INIT USER
    # --------------------------
    if user not in data[today]["users"]:

        data[today]["users"][user] = {

            # Tasks
            "quiz": 0,
            "answer": 0,
            "comment": 0,
            "daily_mcq": 0,
            "daily_mains": 0,

            # Completion
            "completed": False,

            # XP
            "xp_earned": 0
        }

        save_daily(data)

    return data


# ==============================
# UPDATE TASK
# ==============================
def update_task(user, task, xp=0):

    data = init_user_daily(user)

    today = get_today()

    user_data = data[today]["users"][user]

    # --------------------------
    # SAFE TASK INIT
    # --------------------------
    if task not in user_data:

        user_data[task] = 0

    # --------------------------
    # UPDATE TASK
    # --------------------------
    user_data[task] += 1

    # --------------------------
    # XP
    # --------------------------
    user_data["xp_earned"] += xp

    # --------------------------
    # COMPLETION LOGIC
    # --------------------------
    conditions = [

        user_data["quiz"] >= 1,

        user_data["answer"] >= 1,

        user_data["comment"] >= 2
    ]

    if all(conditions):

        user_data["completed"] = True

    save_daily(data)

    return user_data


# ==============================
# GET USER DAILY
# ==============================
def get_user_daily(user):

    data = init_user_daily(user)

    today = get_today()

    return data[today]["users"][user]


# ==============================
# CHECK DAILY COMPLETE
# ==============================
def is_daily_completed(user):

    data = init_user_daily(user)

    today = get_today()

    return data[today]["users"][user]["completed"]


# ==============================
# GET DAILY STATS
# ==============================
def get_daily_stats():

    data = load_daily()

    today = get_today()

    if today not in data:

        return {
            "users": 0,
            "completed": 0
        }

    users = data[today].get("users", {})

    total_users = len(users)

    completed = len([
        u for u in users.values()
        if u.get("completed")
    ])

    return {
        "users": total_users,
        "completed": completed
    }


# ==============================
# DAILY LEADERBOARD
# ==============================
def get_daily_leaderboard(limit=10):

    data = load_daily()

    today = get_today()

    if today not in data:

        return []

    users = data[today].get("users", {})

    leaderboard = []

    for username, stats in users.items():

        leaderboard.append({

            "user": username,

            "xp":
            stats.get("xp_earned", 0),

            "completed":
            stats.get("completed", False)
        })

    leaderboard = sorted(
        leaderboard,
        key=lambda x: x["xp"],
        reverse=True
    )

    return leaderboard[:limit]