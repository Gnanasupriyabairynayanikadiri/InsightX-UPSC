from app.database.connection import SessionLocal
from app.services.auth_service import decode_token

from fastapi import Header, HTTPException


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Header(None)):

    if not authorization:
        return None

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            return None

        return decode_token(token)

    except:
        return None
