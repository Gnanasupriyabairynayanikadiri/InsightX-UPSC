# =====================================================
# 📁 FILE: core/study_os/timetable_generator.py
# AI SMART EDITABLE TIMETABLE GENERATOR
# =====================================================

import os
import json


# =====================================================
# STORAGE
# =====================================================

TIMETABLE_FILE = "storage/timetable_data.json"


# =====================================================
# ENSURE STORAGE
# =====================================================

def ensure_storage():

    os.makedirs(
        "storage",
        exist_ok=True
    )

    if not os.path.exists(TIMETABLE_FILE):

        with open(
            TIMETABLE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump({}, f)


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    ensure_storage()

    try:

        with open(
            TIMETABLE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

            return {}

    except Exception:
        return {}


# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):

    ensure_storage()

    with open(
        TIMETABLE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# NORMALIZE USER
# =====================================================

def normalize_user(user):

    if not user:
        return "guest"

    return str(user).strip().lower()


# =====================================================
# AI DAILY TIMETABLE
# =====================================================

def generate_daily_timetable(
    weak_subject="Polity",
    study_hours=8,
    focus_mode="Balanced"
):

    subjects = [

        f"📚 {weak_subject} Deep Study",

        "📰 Current Affairs",

        "🧠 MCQ Practice",

        "✍️ Answer Writing",

        "🔁 Revision",

        "📖 Optional Subject",

        "📘 NCERT Reading",

        "📊 PYQ Analysis"
    ]

    if focus_mode == "Deep Work":

        subjects.insert(
            0,
            "🎯 Deep Focus Session"
        )

    timetable = []

    start_hour = 5

    for i in range(study_hours):

        timetable.append({

            "start": f"{start_hour + i}:00",

            "end": f"{start_hour + i + 1}:00",

            "task": subjects[
                i % len(subjects)
            ]
        })

    return timetable


# =====================================================
# CUSTOM TIMETABLE
# =====================================================

def generate_custom_timetable(
    study_hours=8
):

    tasks = [

        "📚 Static Subjects",

        "🧠 MCQ Practice",

        "✍️ Answer Writing",

        "📰 Current Affairs",

        "🔁 Revision",

        "📖 Optional Subject",

        "📊 PYQ Analysis",

        "📘 NCERT Revision"
    ]

    timetable = []

    start_hour = 6

    for i in range(study_hours):

        timetable.append({

            "start": f"{start_hour + i}:00",

            "end": f"{start_hour + i + 1}:00",

            "task": tasks[
                i % len(tasks)
            ]
        })

    return timetable


# =====================================================
# GET USER TIMETABLE
# =====================================================

def get_user_timetable(user):

    user = normalize_user(user)

    data = load_data()

    if user not in data:

        data[user] = generate_daily_timetable()

        save_data(data)

    return data[user]


# =====================================================
# UPDATE USER TIMETABLE
# =====================================================

def update_user_timetable(
    user,
    timetable
):

    user = normalize_user(user)

    data = load_data()

    data[user] = timetable

    save_data(data)


# =====================================================
# ADD TIMETABLE BLOCK
# =====================================================

def add_timetable_block(
    user,
    start,
    end,
    task
):

    timetable = get_user_timetable(user)

    timetable.append({

        "start": start,

        "end": end,

        "task": task
    })

    update_user_timetable(
        user,
        timetable
    )


# =====================================================
# DELETE TIMETABLE BLOCK
# =====================================================

def delete_timetable_block(
    user,
    index
):

    timetable = get_user_timetable(user)

    if 0 <= index < len(timetable):

        timetable.pop(index)

    update_user_timetable(
        user,
        timetable
    )


# =====================================================
# AI SUGGESTIONS
# =====================================================

def get_ai_timetable_suggestion(
    user,
    weak_subject="Economy",
    productivity="Medium"
):

    suggestions = []

    if productivity == "High":

        suggestions.extend([

            "🎯 Add 2-hour Deep Work block",

            "🧠 Increase MCQ practice",

            "✍️ Add extra answer writing session"
        ])

    elif productivity == "Low":

        suggestions.extend([

            "🔁 Increase revision sessions",

            "📘 Short NCERT study blocks",

            "⏳ Use Pomodoro sessions"
        ])

    else:

        suggestions.extend([

            "📚 Balanced GS preparation",

            "🧠 Daily MCQ practice",

            "📰 Current Affairs consistency"
        ])

    suggestions.append(

        f"⚠️ Focus more on {weak_subject}"
    )

    return suggestions


# =====================================================
# WEEKEND TIMETABLE
# =====================================================

def generate_weekend_timetable():

    return [

        {
            "start": "7:00",
            "end": "10:00",
            "task": "🧠 Full Mock Test"
        },

        {
            "start": "11:00",
            "end": "13:00",
            "task": "📊 Mock Analysis"
        },

        {
            "start": "14:00",
            "end": "16:00",
            "task": "🔁 Weekly Revision"
        },

        {
            "start": "17:00",
            "end": "19:00",
            "task": "✍️ Essay Writing"
        }
    ]