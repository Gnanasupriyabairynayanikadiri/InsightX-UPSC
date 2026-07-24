# =========================================================
# FILE: backend/app/api/routes/current_affairs.py
# CURRENT AFFAIRS API
# =========================================================

print("✅ CURRENT_AFFAIRS ROUTE LOADED")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.database.connection import SessionLocal
from app.database.models import CurrentAffairs
from app.database.repository import CurrentAffairsRepository
from app.services.static_linker import detect_category
from app.fetchers.news_fetcher import fetch_daily_news

from app.services.processor import (
    process_daily_news,
    process_news_item
)

router = APIRouter(
    prefix="/ca",
    tags=["Current Affairs"]
)

# =========================================================
# GET DAILY CURRENT AFFAIRS
# =========================================================

@router.get("/daily")
def get_daily_ca(
    db: Session = Depends(get_db)
):

    try:

        print("\n========== DAILY CA REQUEST ==========")

        data = CurrentAffairsRepository.get_all_ca(
            db=db,
            limit=20
        )

        print(
            f"TOTAL ITEMS FOUND = {len(data)}"
        )

        return {
            "status": "success",
            "count": len(data),
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "source": item.source,
                    "link": item.link,
                    "category": item.category,
                    "importance": item.importance,
                    "quick_summary": item.quick_summary,
                    "background": item.background,
                    "prelims_focus": item.prelims_focus,
                    "mains_question": item.mains_question,
                    "relevance_score": item.relevance_score,
                    "upsc_score": item.upsc_score,
                    "gs_paper": item.gs_paper,
                    "insight": item.insight
                }
                for item in data
            ]
        }

    except Exception as e:

        print(
            f"[DAILY CA ERROR] {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# REFRESH CURRENT AFFAIRS
# =========================================================

@router.post("/refresh")
def refresh_ca():

    try:

        print(
            "\n========== REFRESH ROUTE HIT =========="
        )

        processed = process_daily_news()

        print(
            f"PROCESSED COUNT = {len(processed)}"
        )

        print(
            "========== REFRESH COMPLETE ==========\n"
        )

        return {
            "status": "updated",
            "items": len(processed)
        }

    except Exception as e:

        print(
            f"[REFRESH ERROR] {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# BASIC TEST
# =========================================================

@router.get("/test")
def test_route():

    print("TEST ROUTE EXECUTED")

    return {
        "status": "working"
    }

# =========================================================
# ROUTER DEBUG
# =========================================================

@router.get("/debug")
def debug_route():

    return {
        "router_loaded": True,
        "refresh_route_available": True,
        "daily_route_available": True
    }

# =========================================================
# FETCHER TEST
# =========================================================

@router.get("/fetch-test")
def fetch_test():

    try:

        data = fetch_daily_news()

        return {
            "count": len(data),
            "data": data
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================================================
# PROCESSOR TEST
# =========================================================

@router.get("/processor-test")
def processor_test():

    db = SessionLocal()

    try:

        count = (
            db.query(CurrentAffairs)
            .count()
        )

        return {
            "count": count
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        db.close()

# =========================================================
# SINGLE ARTICLE TEST
# =========================================================

@router.get("/single-test")
def single_test():

    from app.database.connection import SessionLocal
    from app.services.processor import (
        detect_category,
        generate_editorial_summary,
        generate_background,
        generate_prelims_focus,
        generate_mains_question,
        generate_tags,
        map_pyq_references
    )

    db = SessionLocal()

    try:

        title = "TEST ARTICLE UNIQUE 999999"
        category = detect_category(title, "")

        return {
            "category_type": str(type(category)),
            "summary_type": str(type(generate_editorial_summary(title, category))),
            "background_type": str(type(generate_background(title, category))),
            "prelims_type": str(type(generate_prelims_focus(title, category))),
            "mains_type": str(type(generate_mains_question(title, category))),
            "tags_type": str(type(generate_tags(title, category))),
            "pyq_type": str(type(map_pyq_references(title, category))),
            "background": str(generate_background(title, category))[:300],
            "prelims": str(generate_prelims_focus(title, category))[:300],
            "tags": str(generate_tags(title, category))[:300],
            "pyq": str(map_pyq_references(title, category))[:300]
        }

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
        }

    finally:
        db.close()

@router.get("/save-test")
def save_test():

    from app.database.connection import SessionLocal
    from app.database.repository import CurrentAffairsRepository

    db = SessionLocal()

    try:

        data = {
            "content_hash": "test123456789",
            "title": "Save Test",
            "description": "Testing save",
            "source": "Test",
            "link": "https://test.com",
            "category": "Polity",
            "importance": "High",
            "quick_summary": "Test summary",
            "background": "Test background",
            "prelims_focus": ["A", "B"],
            "mains_question": "Test question",
            "mcqs": [],
            "tags": ["Polity"],
            "pyq_links": [],
            "relevance_score": 50,
            "upsc_score": 80,
            "gs_paper": "GS2",
            "insight": "Test insight"
        }

        result = CurrentAffairsRepository.create_ca(
            db,
            data
        )

        return {
            "saved": result is not None,
            "id": result.id if result else None
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "error": str(e)
        }

    finally:

        db.close()

@router.get("/db-count")
def db_count():

    db = SessionLocal()

    try:

        count = (
            db.query(CurrentAffairs)
            .count()
        )

        return {
            "count": count
        }

    finally:

        db.close()

@router.get("/category-test")
def category_test():

    from app.services.static_linker import detect_category

    return {
        "iran": detect_category(
            "Iran-U.S war",
            ""
        ),

        "bangladesh": detect_category(
            "Bangladesh PM adviser calls India partner",
            ""
        ),

        "sweden": detect_category(
            "Russia NATO conflict",
            ""
        )
    }

@router.delete("/clear")
def clear_ca():

    db = SessionLocal()

    try:
        CurrentAffairsRepository.delete_all_ca(db)
        return {"status": "cleared"}

    finally:
        db.close()