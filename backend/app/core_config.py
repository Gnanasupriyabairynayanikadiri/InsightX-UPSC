# =========================================================
# 📁 FILE: backend/app/core_config.py
# CENTRAL CONFIGURATION (PRODUCTION READY)
# =========================================================

import os


# =========================================================
# 🌐 PROJECT METADATA
# =========================================================
APP_NAME = "UPSC Insight API"
VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENV", "development")


# =========================================================
# 🗄️ DATABASE CONFIG
# =========================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./insight.db"
)


# =========================================================
# 📰 NEWS API CONFIG
# =========================================================
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

NEWS_API_KEY = os.getenv(
    "NEWS_API_KEY",
    "YOUR_NEWS_API_KEY"
)

NEWS_COUNTRY = "in"
NEWS_PAGE_SIZE = 20


# =========================================================
# ⏱️ SCHEDULER CONFIG
# =========================================================
DAILY_REFRESH_HOURS = int(os.getenv("DAILY_REFRESH_HOURS", "24"))


# =========================================================
# 🔐 SECURITY CONFIG (FUTURE USE)
# =========================================================
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_SECRET")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# =========================================================
# ⚙️ SYSTEM FLAGS
# =========================================================
ENABLE_SCHEDULER = True
ENABLE_AUTO_FETCH = True
DEBUG = ENVIRONMENT == "development"
