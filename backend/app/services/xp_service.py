from sqlalchemy.orm import Session
from app.database.repository import UserRepository


# =========================================================
# ⭐ ADD XP
# =========================================================
def add_xp(db: Session, user_id: int, points: int = 10):

    user = UserRepository.update_xp(db, user_id, points)

    return {
        "user_id": user.id,
        "xp": user.xp,
        "message": f"+{points} XP awarded"
    }


# =========================================================
# 🔥 LOGIN STREAK UPDATE (SIMPLE VERSION)
# =========================================================
def update_streak(db: Session, user_id: int):

    user = UserRepository.get_user_by_id(db, user_id)

    if user:
        user.streak += 1
        db.commit()

    return user
