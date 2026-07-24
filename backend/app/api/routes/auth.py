# =========================================================
# 📁 FILE: backend/app/api/routes/auth.py
# AUTH SYSTEM (REGISTER + LOGIN + JWT)
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.database.repository import UserRepository

from app.services.auth_service import (
    verify_password,
    create_access_token,
    hash_password
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================================================
# 📝 REGISTER USER
# =========================================================
@router.post("/register")
def register(
    username: str,
    password: str,
    goal: str,
    db: Session = Depends(get_db)
):

    existing_user = UserRepository.get_user_by_username(db, username)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_pw = hash_password(password)

    user = UserRepository.create_user(
        db=db,
        username=username,
        password=hashed_pw,
        goal=goal
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "goal": user.goal,
            "xp": user.xp
        }
    }


# =========================================================
# 🔐 LOGIN USER
# =========================================================
@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = UserRepository.get_user_by_username(db, username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "user_id": user.id,
        "username": user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "xp": user.xp,
            "goal": user.goal
        }
    }


# =========================================================
# 👤 GET CURRENT USER (JWT TEST ENDPOINT)
# =========================================================
@router.get("/me")
def get_me(current_user: dict = Depends(get_db)):

    return {
        "message": "Token working",
        "user": current_user
    }
