print("✅ MAIN.PY LOADED")

from fastapi import FastAPI

from app.database.init_db import init_db
from app.api.routes.current_affairs import router as ca_router

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="UPSC Insight API",
    version="1.0.0"
)

# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
def startup():

    print("🚀 Initializing Database...")
    init_db()
    print("✅ Database Initialized")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "message": "UPSC Insight API Running"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =====================================================
# ROUTERS
# =====================================================

app.include_router(ca_router)
