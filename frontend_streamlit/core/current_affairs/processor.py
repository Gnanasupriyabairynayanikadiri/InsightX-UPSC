# =========================================================
# FILE: app/services/processor.py
# UPSC CURRENT AFFAIRS PROCESSOR
# =========================================================

import hashlib
import json
import traceback

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.repository import CurrentAffairsRepository

from app.fetchers.news_fetcher import fetch_daily_news

from app.services.article_analyzer import (
    detect_category,
    should_ignore_article,
    GS_PAPER
)

from app.services.relevance_filter import is_upsc_relevant

from app.services.duplicate_detector import is_duplicate

from app.services.relevance import (
    calculate_relevance_score,
    get_importance
)

from app.services.editorial_engine import generate_editorial

from app.services.upsc_enrichment import (
    generate_background,
    generate_prelims_focus,
    generate_mains_question,
    generate_tags
)

from app.services.pyq_mapper import map_pyq_references

from app.services.upsc_score_engine import calculate_upsc_score

from app.services.ranker import generate_insight

print("\n===================================")
print(" UPSC PROCESSOR LOADED ")
print("===================================\n")


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):
    if text is None:
        return ""
    return " ".join(str(text).split())


# =========================================================
# CONTENT HASH
# =========================================================

def generate_hash(title, description, source):
    raw = f"{title}-{description}-{source}"
    return hashlib.md5(raw.encode()).hexdigest()


# =========================================================
# SAFE JSON
# =========================================================

def safe_json(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return [json.dumps(value)]

    return [str(value)]


# =========================================================
# INDIA CHECK
# =========================================================

def is_india_related(title, description):

    text = f"{title} {description}".lower()

    keywords = [
        "india",
        "indian",
        "modi",
        "new delhi",
        "government of india",
        "parliament",
        "supreme court"
    ]

    return any(word in text for word in keywords)


# =========================================================
# GOVERNMENT CHECK
# =========================================================

def is_government_related(title, description):

    text = f"{title} {description}".lower()

    keywords = [
        "government",
        "ministry",
        "cabinet",
        "policy",
        "scheme",
        "mission",
        "act",
        "bill",
        "rbi",
        "isro"
    ]

    return any(word in text for word in keywords)

# =========================================================
# PROCESS SINGLE ARTICLE
# =========================================================

def process_news_item(news, db: Session):

    try:

        # ---------------------------------------
        # Extract fields
        # ---------------------------------------

        title = clean_text(news.get("title"))
        description = clean_text(news.get("description"))

        source = clean_text(
            news.get("source")
            or news.get("source_name")
            or "Unknown"
        )

        link = clean_text(news.get("link"))

        if not title:
            print("[SKIPPED] Empty Title")
            return None

        print("\n========================================")
        print("ARTICLE :", title)

        # ---------------------------------------
        # Ignore sports / entertainment
        # ---------------------------------------

        if should_ignore_article(title, description):
            print("[IGNORED ARTICLE]")
            return None

        # ---------------------------------------
        # Hash duplicate
        # ---------------------------------------

        content_hash = generate_hash(
            title,
            description,
            source
        )

        existing = CurrentAffairsRepository.get_by_hash(
            db,
            content_hash
        )

        if existing:
            print("[HASH DUPLICATE]")
            return None

        # ---------------------------------------
        # UPSC relevance filter
        # ---------------------------------------

        relevant, reason = is_upsc_relevant(
            title,
            description,
            source
        )

        if not relevant:
            print("[FILTERED]", reason)
            return None

        # ---------------------------------------
        # Category
        # ---------------------------------------

        category = detect_category(
            title,
            description
        )

        if category == "Misc":
            print("[MISC CATEGORY]")
            return None

        # ---------------------------------------
        # Relevance
        # ---------------------------------------

        relevance_score = calculate_relevance_score(
            title=title,
            summary=description,
            category=category
        )

        print("Category :", category)
        print("Relevance :", relevance_score)

        if relevance_score < 40:
            print("[LOW RELEVANCE]")
            return None

        # ---------------------------------------
        # Semantic Duplicate
        # ---------------------------------------

        recent_titles = CurrentAffairsRepository.get_recent_titles(db)

        duplicate, old_title, score = is_duplicate(
            title,
            recent_titles
        )

        if duplicate:
            print("[SEMANTIC DUPLICATE]")
            print("OLD :", old_title)
            print("SIM :", round(score, 2))
            return None

        # ---------------------------------------
        # Importance
        # ---------------------------------------

        importance = get_importance(
            title=title,
            summary=description,
            category=category
        )

        # ---------------------------------------
        # Editorial
        # ---------------------------------------

        quick_summary = generate_editorial(
            title,
            category
        )

        # ---------------------------------------
        # UPSC Enrichment
        # ---------------------------------------

        background = generate_background(
            title,
            category
        )

        prelims_focus = generate_prelims_focus(
            title,
            category
        )

        mains_question = generate_mains_question(
            title,
            category
        )

        tags = generate_tags(
            title,
            category
        )

        pyq_links = map_pyq_references(
            title,
            category
        )

        # ---------------------------------------
        # India / Government
        # ---------------------------------------

        india_related = is_india_related(
            title,
            description
        )

        government_related = is_government_related(
            title,
            description
        )

        print("----------------------------------------")
        print("Importance :", importance)
        print("----------------------------------------")

                # ---------------------------------------
        # UPSC SCORE
        # ---------------------------------------

        upsc_score = calculate_upsc_score(

            category=category,
            relevance_score=relevance_score,
            source=source,
            importance=importance,
            india_related=india_related,
            government_related=government_related

        )

        print("UPSC Score :", upsc_score)

        if upsc_score < 70:

            print("[LOW UPSC SCORE]")

            return None

        # ---------------------------------------
        # GS PAPER
        # ---------------------------------------

        gs_paper = GS_PAPER.get(
            category,
            "GS2"
        )

        # ---------------------------------------
        # INSIGHT
        # ---------------------------------------

        insight = generate_insight(
            title,
            category
        )

        print("----------------------------------------")
        print("GS Paper :", gs_paper)
        print("----------------------------------------")

        # ---------------------------------------
        # DATABASE OBJECT
        # ---------------------------------------

        ca_data = {

            "content_hash": content_hash,

            "title": title,

            "description": description,

            "source": source,

            "link": link,

            "category": category,

            "importance": importance,

            "quick_summary": quick_summary,

            "background": background,

            "prelims_focus": safe_json(prelims_focus),

            "mains_question": mains_question,

            "mcqs": [],

            "tags": safe_json(tags),

            "pyq_links": safe_json(pyq_links),

            "relevance_score": relevance_score,

            "upsc_score": upsc_score,

            "gs_paper": gs_paper,

            "insight": insight

        }

        # ---------------------------------------
        # SAVE
        # ---------------------------------------

        result = CurrentAffairsRepository.create_ca(
            db,
            ca_data
        )

        print()
        print("✅ ARTICLE SAVED")
        print("TITLE :", title)
        print("CATEGORY :", category)
        print("UPSC SCORE :", upsc_score)
        print("========================================")

        return result

    except Exception:

        print()
        print("========== PROCESS ERROR ==========")
        traceback.print_exc()
        print("===================================")

        db.rollback()

        return None

# =========================================================
# DAILY PIPELINE
# =========================================================

def process_daily_news():

    print()
    print("========================================")
    print("STARTING DAILY UPSC PIPELINE")
    print("========================================")

    db = SessionLocal()

    try:

        news_list = fetch_daily_news()

        print(f"Fetched {len(news_list)} Articles")

        processed = []

        seen_titles = set()

        for news in news_list:

            title = clean_text(
                news.get("title", "")
            ).lower()

            if not title:
                continue

            if title in seen_titles:
                continue

            seen_titles.add(title)

            article = process_news_item(
                news,
                db
            )

            if article:
                processed.append(article)

        print()
        print("========================================")
        print(f"TOTAL SAVED : {len(processed)}")
        print("PIPELINE COMPLETED")
        print("========================================")

        return processed

    except Exception:

        traceback.print_exc()

        return []

    finally:

        db.close()