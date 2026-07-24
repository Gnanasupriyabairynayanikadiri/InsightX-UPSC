from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.database.repository import BookmarkRepository

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])


# =========================================================
# 🔖 ADD BOOKMARK (PROTECTED)
# =========================================================
@router.post("/add")
def add_bookmark(
    type: str,
    reference_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    return BookmarkRepository.add_bookmark(
        db,
        user_id=user["user_id"],
        type=type,
        reference_id=reference_id
    )
