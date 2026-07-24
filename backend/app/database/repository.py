# =========================================================
# FILE: app/database/repository.py
# DATABASE REPOSITORY
# =========================================================

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.models import CurrentAffairs


class CurrentAffairsRepository:

    # =====================================================
    # CREATE ARTICLE
    # =====================================================

    @staticmethod
    def create_ca(db: Session, data: dict):

        article = CurrentAffairs(**data)

        db.add(article)

        db.commit()

        db.refresh(article)

        return article


    # =====================================================
    # GET USING HASH
    # =====================================================

    @staticmethod
    def get_by_hash(db: Session, content_hash: str):

        return (
            db.query(CurrentAffairs)
            .filter(CurrentAffairs.content_hash == content_hash)
            .first()
        )


    # =====================================================
    # GET BY ID
    # =====================================================

    @staticmethod
    def get_by_id(db: Session, article_id: int):

        return (
            db.query(CurrentAffairs)
            .filter(CurrentAffairs.id == article_id)
            .first()
        )


    # =====================================================
    # GET ALL CURRENT AFFAIRS
    # =====================================================

    @staticmethod
    def get_all_ca(db: Session, limit=None):

        query = (
            db.query(CurrentAffairs)
            .order_by(CurrentAffairs.created_at.desc())
        )

        if limit:
            query = query.limit(limit)

        return query.all()


    # =====================================================
    # GET DAILY FEED
    # =====================================================

    @staticmethod
    def get_daily_feed(db: Session, limit: int = 20):

        return (
            db.query(CurrentAffairs)
            .order_by(
                desc(CurrentAffairs.upsc_score),
                desc(CurrentAffairs.importance),
                desc(CurrentAffairs.id)
            )
            .limit(limit)
            .all()
        )


    # =====================================================
    # GET RECENT TITLES
    # =====================================================

    @staticmethod
    def get_recent_titles(db: Session, limit: int = 300):

        rows = (
            db.query(CurrentAffairs.title)
            .order_by(desc(CurrentAffairs.id))
            .limit(limit)
            .all()
        )

        return [
            row[0]
            for row in rows
            if row[0]
        ]


    # =====================================================
    # GET CATEGORY ARTICLES
    # =====================================================

    @staticmethod
    def get_category(db: Session, category: str, limit: int = 50):

        return (
            db.query(CurrentAffairs)
            .filter(CurrentAffairs.category == category)
            .order_by(desc(CurrentAffairs.upsc_score))
            .limit(limit)
            .all()
        )


    # =====================================================
    # DELETE SINGLE ARTICLE
    # =====================================================

    @staticmethod
    def delete(db: Session, article_id: int):

        article = (
            db.query(CurrentAffairs)
            .filter(CurrentAffairs.id == article_id)
            .first()
        )

        if article:

            db.delete(article)

            db.commit()

            return True

        return False


    # =====================================================
    # DELETE ALL ARTICLES
    # =====================================================

    @staticmethod
    def delete_all_ca(db: Session):

        deleted = db.query(CurrentAffairs).delete()

        db.commit()

        return deleted


    # =====================================================
    # TOTAL COUNT
    # =====================================================

    @staticmethod
    def count(db: Session):

        return db.query(CurrentAffairs).count()