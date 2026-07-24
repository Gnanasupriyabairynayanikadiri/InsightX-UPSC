# =========================================================
# ⭐ XP SYSTEM API (PROTECTED)
# =========================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.database.repository import UserRepository


router = APIRouter(prefix="/xp", tags=["XP"])


# =========================================================
# ⭐ ADD XP (PROTECTED)
# =========================================================
@router.post("/add")
def add_xp(
    xp: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    updated_user = UserRepository.update_xp(
        db,
        user_id=user["user_id"],
        xp=xp
    )

    return {
        "status": "success",
        "xp_added": xp,
        "total_xp": updated_user.xp
    }
