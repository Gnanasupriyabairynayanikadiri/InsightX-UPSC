# =========================================================
# 📁 core/auth.py
# =========================================================

import json
import os

from datetime import date, timedelta


# =========================================================
# 📂 STORAGE FILE
# =========================================================
FILE = "storage/users.json"


# =========================================================
# 📂 ENSURE STORAGE
# =========================================================
def ensure_storage():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FILE):

        with open(FILE, "w") as f:

            json.dump({}, f)


# =========================================================
# 📂 LOAD USERS
# =========================================================
def load_users():

    ensure_storage()

    try:

        with open(FILE, "r") as f:

            return json.load(f)

    except:

        return {}


# =========================================================
# 📂 SAVE USERS
# =========================================================
def save_users(data):

    ensure_storage()

    with open(FILE, "w") as f:

        json.dump(data, f, indent=4)


# =========================================================
# 🔐 REGISTER USER
# =========================================================
def register_user(username, password, goal):

    data = load_users()

    username = username.strip()

    # =====================================================
    # VALIDATION
    # =====================================================
    if not username or not password:

        return False, "Username and password required"

    if len(username) < 3:

        return False, "Username too short"

    if len(password) < 4:

        return False, "Password too short"

    if username in data:

        return False, "User already exists"

    # =====================================================
    # CREATE USER
    # =====================================================
    data[username] = {

        # AUTH
        "password": password,

        # PROFILE
        "goal": goal,

        "created_at": str(date.today()),

        # GAMIFICATION
        "xp": 0,

        "level": 1,

        "coins": 0,

        # STREAK SYSTEM
        "streak": 1,

        "last_active": str(date.today()),

        # DAILY CHALLENGE
        "challenge": None,

        "challenge_date": None,

        # PROGRESS
        "completed": [],

        "bookmarks": [],

        "resume": {},

        # ANALYTICS
        "total_quizzes": 0,

        "correct_answers": 0,

        "answers_written": 0,

        # CSAT
        "csat_progress": {},

        # MAINS
        "mains_progress": {},

        # CURRENT AFFAIRS
        "ca_progress": {}
    }

    save_users(data)

    return True, "Registered successfully"


# =========================================================
# 🔐 LOGIN USER
# =========================================================
def login_user(username, password):

    data = load_users()

    username = username.strip()

    # =====================================================
    # USER NOT FOUND
    # =====================================================
    if username not in data:

        return False, "User not found"

    user = data[username]

    # =====================================================
    # PASSWORD CHECK
    # =====================================================
    if user["password"] != password:

        return False, "Wrong password"

    # =====================================================
    # UPDATE STREAK
    # =====================================================
    update_streak(username)

    # Reload updated data
    data = load_users()

    return True, data[username]


# =========================================================
# 🚪 LOGOUT
# =========================================================
def logout_user():

    return True


# =========================================================
# 🔥 STREAK SYSTEM
# =========================================================
def update_streak(username):

    data = load_users()

    if username not in data:

        return

    user = data[username]

    today = date.today()

    last_active = user.get("last_active")

    try:

        last_date = date.fromisoformat(last_active)

    except:

        last_date = today

    # =====================================================
    # SAME DAY
    # =====================================================
    if last_date == today:

        return

    # =====================================================
    # CONTINUED STREAK
    # =====================================================
    if last_date == today - timedelta(days=1):

        user["streak"] += 1

    # =====================================================
    # STREAK RESET
    # =====================================================
    else:

        user["streak"] = 1

    user["last_active"] = str(today)

    save_users(data)


# =========================================================
# ⭐ XP SYSTEM
# =========================================================
def add_xp(username, xp):

    data = load_users()

    if username not in data:

        return

    user = data[username]

    user["xp"] += xp

    # =====================================================
    # LEVEL SYSTEM
    # =====================================================
    user["level"] = (user["xp"] // 100) + 1

    save_users(data)


# =========================================================
# 🪙 COINS SYSTEM
# =========================================================
def add_coins(username, coins):

    data = load_users()

    if username not in data:

        return

    data[username]["coins"] += coins

    save_users(data)


# =========================================================
# 📊 UPDATE QUIZ STATS
# =========================================================
def update_quiz_stats(username, total, correct):

    data = load_users()

    if username not in data:

        return

    user = data[username]

    user["total_quizzes"] += total

    user["correct_answers"] += correct

    save_users(data)


# =========================================================
# 📈 GET USER STATS
# =========================================================
def get_user_stats(username):

    data = load_users()

    if username not in data:

        return {}

    user = data[username]

    total = user.get("total_quizzes", 0)

    correct = user.get("correct_answers", 0)

    accuracy = 0

    if total > 0:

        accuracy = round(
            (correct / total) * 100,
            2
        )

    return {

        "xp": user.get("xp", 0),

        "level": user.get("level", 1),

        "coins": user.get("coins", 0),

        "streak": user.get("streak", 0),

        "accuracy": accuracy,

        "answers_written": user.get(
            "answers_written",
            0
        )
    }


# =========================================================
# 📌 SAVE BOOKMARK
# =========================================================
def save_bookmark(username, bookmark):

    data = load_users()

    if username not in data:

        return

    bookmarks = data[username].get(
        "bookmarks",
        []
    )

    if bookmark not in bookmarks:

        bookmarks.append(bookmark)

    data[username]["bookmarks"] = bookmarks

    save_users(data)


# =========================================================
# 📌 LOAD BOOKMARKS
# =========================================================
def load_bookmarks(username):

    data = load_users()

    if username not in data:

        return []

    return data[username].get(
        "bookmarks",
        []
    )


# =========================================================
# 🔁 SAVE RESUME
# =========================================================
def save_resume(username, resume_data):

    data = load_users()

    if username not in data:

        return

    data[username]["resume"] = resume_data

    save_users(data)


# =========================================================
# 🔁 LOAD RESUME
# =========================================================
def load_resume(username):

    data = load_users()

    if username not in data:

        return {}

    return data[username].get(
        "resume",
        {}
    )