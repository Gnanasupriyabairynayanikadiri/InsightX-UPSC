# =========================================================
# 🎮 GAMIFICATION ENGINE (XP + LEVEL + STREAK)
# =========================================================

from app.database.repository import UserRepository


# =========================================================
# ⭐ XP RULES CONFIG
# =========================================================
XP_RULES = {
    "ca_read": 5,
    "quiz_attempt": 10,
    "correct_answer": 2,
    "perfect_score_bonus": 20
}


# =========================================================
# ⭐ CALCULATE LEVEL
# =========================================================
def calculate_level(xp: int):

    return (xp // 100) + 1


# =========================================================
# ⭐ APPLY XP TO USER
# =========================================================
def add_xp(db, user_id: int, xp: int):

    user = UserRepository.update_xp(db, user_id, xp)

    level = calculate_level(user.xp)

    return {
        "xp_added": xp,
        "total_xp": user.xp,
        "level": level
    }


# =========================================================
# 📰 CA REWARD
# =========================================================
def reward_ca_read(db, user_id: int):

    return add_xp(
        db,
        user_id,
        XP_RULES["ca_read"]
    )


# =========================================================
# 🧠 QUIZ REWARD SYSTEM
# =========================================================
def reward_quiz(db, user_id: int, score: int, total: int):

    base_xp = XP_RULES["quiz_attempt"]

    correct_xp = score * XP_RULES["correct_answer"]

    bonus = 0

    if score == total:
        bonus = XP_RULES["perfect_score_bonus"]

    total_xp = base_xp + correct_xp + bonus

    return add_xp(db, user_id, total_xp)
