# =========================================================
# FILE: app/services/article_storage.py
# UPSC ARTICLE STORAGE
# =========================================================

from sqlalchemy import text
from app.database.db import engine


# =========================================================
# CHECK ARTICLE EXISTS
# =========================================================

def article_exists(title):

    query = text("""
        SELECT COUNT(*)
        FROM current_affairs_articles
        WHERE title = :title
    """)

    try:

        with engine.connect() as conn:

            count = conn.execute(
                query,
                {"title": title}
            ).scalar()

        return count > 0

    except Exception as e:

        print(f"❌ article_exists Error: {e}")
        return False


# =========================================================
# SAVE ARTICLE
# =========================================================

def save_article(article):

    query = text("""
        INSERT INTO current_affairs_articles
        (
            article_date,
            title,
            category,
            source_name,
            article_url,
            summary,
            full_analysis,
            relevance_score,
            upsc_score,
            importance_level,
            gs_paper,
            prelims_focus,
            mains_focus,
            practice_question,
            created_at
        )

        VALUES
        (
            :article_date,
            :title,
            :category,
            :source_name,
            :article_url,
            :summary,
            :full_analysis,
            :relevance_score,
            :upsc_score,
            :importance_level,
            :gs_paper,
            :prelims_focus,
            :mains_focus,
            :practice_question,
            GETDATE()
        )
    """)

    payload = {

        "article_date":
            article.get("article_date"),

        "title":
            article.get("title", "No Title"),

        "category":
            article.get("category", "Current Affairs"),

        "source_name":
            article.get("source_name", "Unknown"),

        "article_url":
            article.get("article_url", ""),

        "summary":
            article.get("summary", ""),

        "full_analysis":
            article.get("full_analysis", ""),

        "relevance_score":
            article.get("relevance_score", 50),

        "upsc_score":
            article.get("upsc_score", 50),

        "importance_level":
            article.get("importance_level", "Medium"),

        "gs_paper":
            article.get("gs_paper", ""),

        "prelims_focus":
            article.get("prelims_focus", ""),

        "mains_focus":
            article.get("mains_focus", ""),

        "practice_question":
            article.get("practice_question", "")
    }

    try:

        with engine.begin() as conn:

            conn.execute(
                query,
                payload
            )

        print(f"✅ Saved: {payload['title']}")

        return True

    except Exception as e:

        print(f"❌ Save Failed: {payload['title']}")
        print(e)

        return False


# =========================================================
# SAVE ONLY IF NOT EXISTS
# =========================================================

def save_if_not_exists(article):

    title = article.get("title", "")

    if not title:

        print("⚠️ Empty title skipped")
        return False

    if article_exists(title):

        print(f"⚠️ Already Exists: {title}")
        return False

    return save_article(article)


# =========================================================
# GET ARTICLES BY MONTH
# =========================================================

def get_articles_by_month(month, year):

    query = text("""
        SELECT *
        FROM current_affairs_articles
        WHERE MONTH(article_date)=:month
        AND YEAR(article_date)=:year
        ORDER BY article_date DESC
    """)

    try:

        with engine.connect() as conn:

            result = conn.execute(
                query,
                {
                    "month": month,
                    "year": year
                }
            )

            return result.fetchall()

    except Exception as e:

        print(f"❌ get_articles_by_month Error: {e}")
        return []


# =========================================================
# GET ALL ARTICLES
# =========================================================

def get_all_articles():

    query = text("""
        SELECT *
        FROM current_affairs_articles
        ORDER BY article_date DESC
    """)

    try:

        with engine.connect() as conn:

            result = conn.execute(query)

            return result.fetchall()

    except Exception as e:

        print(f"❌ get_all_articles Error: {e}")
        return []


# =========================================================
# DELETE ARTICLE
# =========================================================

def delete_article(article_id):

    query = text("""
        DELETE
        FROM current_affairs_articles
        WHERE id=:article_id
    """)

    try:

        with engine.begin() as conn:

            conn.execute(
                query,
                {
                    "article_id": article_id
                }
            )

        print("🗑️ Article Deleted")

        return True

    except Exception as e:

        print(f"❌ Delete Error: {e}")
        return False


# =========================================================
# ARTICLE COUNT
# =========================================================

def get_article_count():

    query = text("""
        SELECT COUNT(*)
        FROM current_affairs_articles
    """)

    try:

        with engine.connect() as conn:

            count = conn.execute(query).scalar()

        return count

    except Exception as e:

        print(f"❌ Count Error: {e}")
        return 0


# =========================================================
# GET LATEST ARTICLES
# =========================================================

def get_latest_articles(limit=10):

    query = text(f"""
        SELECT TOP {limit}
            id,
            article_date,
            title,
            category,
            source_name,
            importance_level,
            relevance_score,
            upsc_score,
            gs_paper
        FROM current_affairs_articles
        ORDER BY id DESC
    """)

    try:

        with engine.connect() as conn:

            result = conn.execute(query)

            return result.fetchall()

    except Exception as e:

        print(f"❌ Latest Articles Error: {e}")
        return []