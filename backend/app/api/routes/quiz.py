# =========================================================
# 🧠 QUIZ API (PROTECTED + GAMIFIED)
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict

from app.api.dependencies import get_db, get_current_user
from app.database.repository import QuizRepository

from app.services.gamification_service import reward_quiz


router = APIRouter(prefix="/quiz", tags=["Quiz"])


# =========================================================
# 📦 REQUEST SCHEMA (CLEAN INPUT VALIDATION)
# =========================================================
class QuizSubmitRequest(BaseModel):
    score: int
    total: int
    topic: str
    answers: Dict


# =========================================================
# 🧠 SAVE QUIZ RESULT + XP REWARD
# =========================================================
@router.post("/submit")
def submit_quiz(
    payload: QuizSubmitRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):

    try:
        # -----------------------------------------
        # SAVE QUIZ ATTEMPT
        # -----------------------------------------
        attempt = QuizRepository.save_attempt(
            db,
            user_id=user["user_id"],
            score=payload.score,
            total=payload.total,
            topic=payload.topic,
            answers=payload.answers
        )

        # -----------------------------------------
        # GAMIFICATION XP SYSTEM
        # -----------------------------------------
        xp_result = reward_quiz(
            db,
            user["user_id"],
            payload.score,
            payload.total
        )

        return {
            "status": "success",
            "attempt_id": attempt.id,
            "quiz_score": payload.score,
            "total_questions": payload.total,
            "topic": payload.topic,

            # 🎮 GAMIFICATION OUTPUT
            "xp": xp_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quiz submission failed: {str(e)}"
        )
