# =========================================================
# 🔐 AUTH SERVICE (JWT + PASSWORD SECURITY)
# =========================================================

from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from app.core_config import JWT_SECRET, JWT_ALGORITHM


# =========================================================
# 🔑 PASSWORD HASHING SETUP
# =========================================================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================================
# 🔒 HASH PASSWORD
# =========================================================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# =========================================================
# 🔓 VERIFY PASSWORD
# =========================================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# =========================================================
# 🪪 CREATE JWT TOKEN
# =========================================================
def create_access_token(
    data: dict,
    expires_minutes: int = 60 * 24  # 1 day default
) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token


# =========================================================
# 🔍 DECODE JWT TOKEN
# =========================================================
def decode_token(token: str):

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# =========================================================
# 👤 GET USER FROM TOKEN (HELPER)
# =========================================================
def get_user_from_token(token: str):

    payload = decode_token(token)

    if not payload:
        return None

    return {
        "user_id": payload.get("user_id"),
        "username": payload.get("username")
    }
