# =========================================================
# 📁 FILE: core/xp.py (FINAL STABLE CLEAN VERSION)
# =========================================================

import json
import os
from datetime import datetime

XP_FILE = "data/xp_data.json"


# =========================================================
# INIT
# =========================================================
def initialize_xp_system():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(XP_FILE):
        with open(XP_FILE, "w") as f:
            json.dump({}, f)


# =========================================================
# LOAD / SAVE
# =========================================================
def load_users():
    initialize_xp_system()

    try:
        with open(XP_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    initialize_xp_system()

    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================================================
# ENSURE USER (FIXED SAFE STRUCTURE)
# =========================================================
def ensure_user(username):
    data = load_users()

    if username not in data:
        data[username] = {
            "xp": 0,
            "level": 1,
            "streak": 0,
            "last_active": "",
            "badges": []
        }
        save_users(data)

    return data


# =========================================================
# LEVEL
# =========================================================
def calculate_level(xp):
    return (xp // 100) + 1


# =========================================================
# XP CORE
# =========================================================
def reward_xp(username, xp_amount):
    data = ensure_user(username)

    data[username]["xp"] += xp_amount
    data[username]["level"] = calculate_level(data[username]["xp"])

    update_streak(username)

    save_users(data)

    return data[username]["xp"]


def add_xp(username, xp_amount):
    return reward_xp(username, xp_amount)


# =========================================================
# GETTERS
# =========================================================
def get_user_xp(username):
    data = ensure_user(username)
    return data[username]["xp"]


def get_xp(username):
    return get_user_xp(username)


def get_user_level(username):
    data = ensure_user(username)
    return data[username]["level"]


def get_level(username_or_xp):
    if isinstance(username_or_xp, (int, float)):
        return calculate_level(username_or_xp)

    return get_user_level(username_or_xp)


# =========================================================
# STREAK
# =========================================================
def get_streak(username):
    data = ensure_user(username)
    return data[username]["streak"]


def update_streak(username):
    data = ensure_user(username)

    today = datetime.now().strftime("%Y-%m-%d")

    if data[username]["last_active"] != today:
        data[username]["streak"] += 1
        data[username]["last_active"] = today

    save_users(data)


# =========================================================
# RANK SYSTEM
# =========================================================
def get_rank(username):
    xp = get_user_xp(username)

    if xp >= 1000:
        return "🏆 UPSC Legend"
    elif xp >= 700:
        return "🥇 UPSC Topper"
    elif xp >= 500:
        return "🔥 Advanced Aspirant"
    elif xp >= 300:
        return "🚀 Intermediate Aspirant"
    elif xp >= 100:
        return "📘 Beginner Aspirant"
    else:
        return "🌱 Starter"


# =========================================================
# LEADERBOARD (FIXED — NO FAKE USERS)
# =========================================================
def get_leaderboard():
    data = load_users()

    leaderboard = []

    for username, info in data.items():

        # ignore corrupted entries
        if not isinstance(info, dict):
            continue

        leaderboard.append({
            "user": username,
            "xp": info.get("xp", 0),
            "level": info.get("level", 1),
            "streak": info.get("streak", 0),
            "rank": get_rank(username)
        })

    leaderboard.sort(key=lambda x: x["xp"], reverse=True)

    return leaderboard


# =========================================================
# USER STATS
# =========================================================
def get_user_stats(username):
    return {
        "xp": get_user_xp(username),
        "streak": get_streak(username)
    }

# =========================================================
# 🔁 BACKWARD COMPATIBILITY (IMPORTANT FIX)
# =========================================================

def reward_user(username, xp_amount):
    """
    Legacy support for old modules like pyq_ui.py
    """
    return reward_xp(username, xp_amount)