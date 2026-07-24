# =========================================================
# FILE: app/database/models.py
# DATABASE MODELS
# =========================================================

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    Text
)

from app.database.connection import Base


# =========================================================
# USER MODEL
# =========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    goal = Column(
        String(255),
        nullable=True
    )

    xp = Column(
        Integer,
        default=0
    )


# =========================================================
# CURRENT AFFAIRS MODEL
# =========================================================

class CurrentAffairs(Base):

    __tablename__ = "current_affairs"

    # -----------------------------------------------------
    # PRIMARY KEY
    # -----------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -----------------------------------------------------
    # DUPLICATE DETECTION
    # -----------------------------------------------------

    content_hash = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        nullable=True
    )

    # -----------------------------------------------------
    # BASIC ARTICLE
    # -----------------------------------------------------

    title = Column(
        String(1000),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    source = Column(
        String(255),
        nullable=True
    )

    link = Column(
        Text,
        nullable=True
    )

    # -----------------------------------------------------
    # UPSC CLASSIFICATION
    # -----------------------------------------------------

    category = Column(
        String(255),
        index=True,
        nullable=True
    )

    importance = Column(
        String(100),
        nullable=True
    )

    gs_paper = Column(
        String(20),
        index=True,
        nullable=True
    )

    # -----------------------------------------------------
    # UPSC ENRICHMENT
    # -----------------------------------------------------

    quick_summary = Column(
        Text,
        nullable=True
    )

    background = Column(
        Text,
        nullable=True
    )

    prelims_focus = Column(
        JSON,
        default=list
    )

    mains_question = Column(
        Text,
        nullable=True
    )

    mcqs = Column(
        JSON,
        default=list
    )

    tags = Column(
        JSON,
        default=list
    )

    pyq_links = Column(
        JSON,
        default=list
    )

    # -----------------------------------------------------
    # SCORING
    # -----------------------------------------------------

    relevance_score = Column(
        Float,
        default=0.0
    )

    upsc_score = Column(
        Float,
        default=0.0,
        index=True
    )

    insight = Column(
        Text,
        nullable=True
    )

    # -----------------------------------------------------
    # TIMESTAMP
    # -----------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )