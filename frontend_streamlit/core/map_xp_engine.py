# =========================================================
# 📁 FILE: core/map_xp_engine.py
# AI UPSC MAP XP ENGINE
# =========================================================

import os
import json

from datetime import datetime


# =========================================================
# 📂 STORAGE CONFIG
# =========================================================

XP_STORAGE_FOLDER = "storage"

XP_FILE = os.path.join(
    XP_STORAGE_FOLDER,
    "map_xp_data.json"
)


# =========================================================
# 📂 INITIALIZE STORAGE
# =========================================================

def initialize_map_xp():

    os.makedirs(
        XP_STORAGE_FOLDER,
        exist_ok=True
    )

    if not os.path.exists(XP_FILE):

        with open(
            XP_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                indent=4
            )


# =========================================================
# 📥 LOAD XP DATA
# =========================================================

def load_map_xp():

    initialize_map_xp()

    try:

        with open(
            XP_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# =========================================================
# 💾 SAVE XP DATA
# =========================================================

def save_map_xp(data):

    initialize_map_xp()

    with open(
        XP_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# 🎯 CREATE USER PROFILE
# =========================================================

def create_map_profile(user):

    data = load_map_xp()

    if user not in data:

        data[user] = {

            "xp": 0,

            "level": 1,

            "correct_answers": 0,

            "wrong_answers": 0,

            "total_questions": 0,

            "streak": 0,

            "max_streak": 0,

            "badges": [],

            "last_played":
                datetime.now().strftime(
                    "%Y-%m-%d"
                ),

            "geo_mastery": {

                "world": 0,

                "india": 0,

                "capitals": 0,

                "rivers": 0,

                "mountains": 0,

                "geopolitics": 0
            }
        }

        save_map_xp(data)

    return data[user]


# =========================================================
# 🏆 LEVEL CALCULATOR
# =========================================================

def calculate_level(xp):

    if xp < 100:

        return 1

    elif xp < 250:

        return 2

    elif xp < 500:

        return 3

    elif xp < 1000:

        return 4

    elif xp < 2000:

        return 5

    elif xp < 5000:

        return 6

    return 7


# =========================================================
# 🎖️ BADGE ENGINE
# =========================================================

def check_badges(profile):

    badges = profile.get(
        "badges",
        []
    )

    correct_answers = profile.get(
        "correct_answers",
        0
    )

    max_streak = profile.get(
        "max_streak",
        0
    )

    xp = profile.get(
        "xp",
        0
    )

    # -----------------------------------------------------
    # FIRST BADGE
    # -----------------------------------------------------

    if (

        correct_answers >= 1

        and "Explorer" not in badges
    ):

        badges.append(
            "Explorer"
        )

    # -----------------------------------------------------
    # MAP LEARNER
    # -----------------------------------------------------

    if (

        correct_answers >= 25

        and "Map Learner" not in badges
    ):

        badges.append(
            "Map Learner"
        )

    # -----------------------------------------------------
    # GEO MASTER
    # -----------------------------------------------------

    if (

        correct_answers >= 100

        and "Geo Master" not in badges
    ):

        badges.append(
            "Geo Master"
        )

    # -----------------------------------------------------
    # STREAK MASTER
    # -----------------------------------------------------

    if (

        max_streak >= 10

        and "Consistency King" not in badges
    ):

        badges.append(
            "Consistency King"
        )

    # -----------------------------------------------------
    # XP MASTER
    # -----------------------------------------------------

    if (

        xp >= 1000

        and "UPSC Cartographer" not in badges
    ):

        badges.append(
            "UPSC Cartographer"
        )

    return badges


# =========================================================
# 🎯 REWARD USER
# =========================================================

def reward_map_user(

    user,
    correct=True,
    category="world",
    difficulty="Easy"
):

    data = load_map_xp()

    profile = create_map_profile(user)

    # -----------------------------------------------------
    # XP SYSTEM
    # -----------------------------------------------------

    xp_gain = 0

    if correct:

        if difficulty == "Easy":

            xp_gain = 5

        elif difficulty == "Medium":

            xp_gain = 10

        else:

            xp_gain = 20

        profile["correct_answers"] += 1

        profile["streak"] += 1

        if (

            profile["streak"]

            > profile["max_streak"]
        ):

            profile["max_streak"] = (

                profile["streak"]
            )

    else:

        xp_gain = 1

        profile["wrong_answers"] += 1

        profile["streak"] = 0

    # -----------------------------------------------------
    # TOTAL QUESTIONS
    # -----------------------------------------------------

    profile["total_questions"] += 1

    # -----------------------------------------------------
    # ADD XP
    # -----------------------------------------------------

    profile["xp"] += xp_gain

    # -----------------------------------------------------
    # UPDATE LEVEL
    # -----------------------------------------------------

    profile["level"] = calculate_level(

        profile["xp"]
    )

    # -----------------------------------------------------
    # CATEGORY MASTERY
    # -----------------------------------------------------

    mastery = profile.get(
        "geo_mastery",
        {}
    )

    if category in mastery and correct:

        mastery[category] += 1

    profile["geo_mastery"] = mastery

    # -----------------------------------------------------
    # LAST PLAYED
    # -----------------------------------------------------

    profile["last_played"] = (

        datetime.now().strftime(
            "%Y-%m-%d"
        )
    )

    # -----------------------------------------------------
    # BADGES
    # -----------------------------------------------------

    profile["badges"] = (

        check_badges(profile)
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    data[user] = profile

    save_map_xp(data)

    return {

        "xp_gained": xp_gain,

        "total_xp": profile["xp"],

        "level": profile["level"],

        "streak": profile["streak"],

        "badges": profile["badges"]
    }


# =========================================================
# 📊 GET USER ANALYTICS
# =========================================================

def get_map_analytics(user):

    data = load_map_xp()

    if user not in data:

        create_map_profile(user)

        data = load_map_xp()

    profile = data[user]

    total_questions = profile.get(
        "total_questions",
        0
    )

    correct_answers = profile.get(
        "correct_answers",
        0
    )

    wrong_answers = profile.get(
        "wrong_answers",
        0
    )

    # -----------------------------------------------------
    # ACCURACY
    # -----------------------------------------------------

    accuracy = 0

    if total_questions > 0:

        accuracy = round(

            (
                correct_answers
                / total_questions
            ) * 100,

            2
        )

    return {

        "xp":
            profile.get("xp", 0),

        "level":
            profile.get("level", 1),

        "correct_answers":
            correct_answers,

        "wrong_answers":
            wrong_answers,

        "total_questions":
            total_questions,

        "accuracy":
            accuracy,

        "streak":
            profile.get("streak", 0),

        "max_streak":
            profile.get("max_streak", 0),

        "badges":
            profile.get("badges", []),

        "geo_mastery":
            profile.get("geo_mastery", {})
    }


# =========================================================
# 🏅 LEADERBOARD
# =========================================================

def get_map_leaderboard():

    data = load_map_xp()

    leaderboard = []

    for user, profile in data.items():

        total_questions = profile.get(
            "total_questions",
            0
        )

        correct_answers = profile.get(
            "correct_answers",
            0
        )

        accuracy = 0

        if total_questions > 0:

            accuracy = round(

                (
                    correct_answers
                    / total_questions
                ) * 100,

                2
            )

        leaderboard.append({

            "user": user,

            "xp": profile.get(
                "xp",
                0
            ),

            "level": profile.get(
                "level",
                1
            ),

            "accuracy": accuracy
        })

    leaderboard = sorted(

        leaderboard,

        key=lambda item: item["xp"],

        reverse=True
    )

    return leaderboard[:10]


# =========================================================
# 🌍 GEO MASTERY LEVEL
# =========================================================

def get_geo_mastery_level(points):

    if points >= 100:

        return "🌟 Expert"

    elif points >= 50:

        return "🔥 Advanced"

    elif points >= 20:

        return "⚡ Intermediate"

    elif points >= 5:

        return "📘 Beginner"

    return "🧭 Starter"


# =========================================================
# 🎯 DAILY MAP CHALLENGE
# =========================================================

def generate_daily_map_challenge():

    challenges = [

        "Identify 5 world capitals",

        "Revise important world straits",

        "Practice Indian states and capitals",

        "Revise neighboring countries of India",

        "Practice rivers and mountains",

        "Revise geopolitical hotspots"
    ]

    return challenges[

        datetime.now().day

        % len(challenges)
    ]


# =========================================================
# 🧪 DEBUG TEST
# =========================================================

if __name__ == "__main__":

    user = "test_user"

    reward_map_user(

        user=user,
        correct=True,
        category="world",
        difficulty="Easy"
    )

    analytics = get_map_analytics(user)

    print(analytics)