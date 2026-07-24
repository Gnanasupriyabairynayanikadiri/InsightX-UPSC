# =====================================================
# FILE: app/database/init_db.py
# DATABASE INITIALIZER
# =====================================================

from app.database.connection import Base, engine

# Import models so SQLAlchemy registers tables
from app.database import models  # noqa: F401


# =====================================================
# INITIALIZE DATABASE
# =====================================================
def init_db():

    print("🔄 Creating database tables...")

    # Uncomment ONLY during development
    # Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    print("✅ Database Created / Synced Successfully")
