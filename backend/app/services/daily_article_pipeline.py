# =========================================================
# FILE: app/services/daily_article_pipeline.py
# UPSC DAILY CURRENT AFFAIRS PIPELINE
# =========================================================

import logging
from datetime import datetime

from app.services.article_fetcher import fetch_articles
from app.services.article_storage import save_if_not_exists
from app.services.monthly_magazine_generator import generate_monthly_magazine

from app.services.article_analyzer import analyze_article
from app.services.relevance import (
    calculate_relevance_score,
    get_importance,
)
from app.services.ranker import (
    calculate_upsc_score,
    classify_gs,
    generate_insight,
)
from app.services.editorial_engine import (
    generate_editorial_structured,
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# PIPELINE
# =========================================================

def run_pipeline():

    start_time = datetime.now()

    logger.info("=" * 70)
    logger.info("🚀 UPSC DAILY CURRENT AFFAIRS PIPELINE STARTED")
    logger.info("=" * 70)

    try:
        articles = fetch_articles()

    except Exception as e:

        logger.exception("Failed to fetch articles")

        return {
            "status": "failed",
            "reason": str(e)
        }

    if not articles:

        logger.warning("No articles received")

        return {
            "status": "no_articles",
            "saved": 0
        }

    logger.info(f"Fetched {len(articles)} articles")

    saved_count = 0
    duplicate_count = 0
    failed_count = 0

    # =====================================================
    # PROCESS EACH ARTICLE
    # =====================================================

    for index, article in enumerate(articles, start=1):

        title = article.get("title", "Untitled")

        logger.info(f"[{index}/{len(articles)}] {title}")

        try:

            # ---------------------------------------------
            # AI ANALYSIS
            # ---------------------------------------------

            analysis = analyze_article(article)

            if analysis is None:
                logger.warning(
                    f"Analyzer returned None. Using defaults for: {title}"
                )

                analysis = {
                    "category": "Current Affairs"
                }

            article.update(analysis)

            # ---------------------------------------------
            # RELEVANCE
            # ---------------------------------------------

            article["relevance_score"] = calculate_relevance_score(
                article["title"],
                article["category"]
            )

            # ---------------------------------------------
            # IMPORTANCE
            # ---------------------------------------------

            article["importance_level"] = get_importance(
                article["title"],
                article["category"]
            )

            # ---------------------------------------------
            # UPSC SCORE
            # ---------------------------------------------

            article["upsc_score"] = calculate_upsc_score(
                article["title"],
                article["category"],
                article["importance_level"],
                article["relevance_score"]
            )

            # ---------------------------------------------
            # GS PAPER
            # ---------------------------------------------

            article["gs_paper"] = classify_gs(
                article["category"]
            )

            # ---------------------------------------------
            # UPSC SUMMARY
            # ---------------------------------------------

            article["summary"] = generate_insight(
                article["title"],
                article["category"]
            )

            # ---------------------------------------------
            # EDITORIAL
            # ---------------------------------------------

            editorial = generate_editorial_structured(
                article["title"],
                article["category"]
            )

            # Store complete editorial as Full Analysis
            article["full_analysis"] = editorial.get("background", "")

            # UPSC fields
            article["prelims_focus"] = editorial.get("prelims_focus", "")

            article["mains_focus"] = editorial.get("mains_focus", "")

            article["practice_question"] = editorial.get("mains_question", "")

            # ---------------------------------------------
            # DEBUG
            # ---------------------------------------------

            logger.info(
                f"GS={article['gs_paper']} | "
                f"Category={article['category']} | "
                f"UPSC={article['upsc_score']}"
            )

            # ---------------------------------------------
            # SAVE
            # ---------------------------------------------

            saved = save_if_not_exists(article)

            if saved:

                saved_count += 1

                logger.info(f"✅ Saved")

            else:

                duplicate_count += 1

                logger.info(f"⚠ Duplicate")

        except Exception:

            failed_count += 1

            logger.exception(f"Failed : {title}")

    # =====================================================
    # MONTHLY MAGAZINE
    # =====================================================

    try:

        month = datetime.now().strftime("%Y-%m")

        logger.info(f"Updating magazine {month}")

        generate_monthly_magazine(month)

        logger.info("Magazine updated")

    except Exception:

        logger.exception("Magazine generation failed")

    # =====================================================
    # SUMMARY
    # =====================================================

    duration = round(
        (datetime.now() - start_time).total_seconds(),
        2
    )

    logger.info("=" * 70)
    logger.info(f"Fetched     : {len(articles)}")
    logger.info(f"Saved       : {saved_count}")
    logger.info(f"Duplicates  : {duplicate_count}")
    logger.info(f"Failed      : {failed_count}")
    logger.info(f"Time        : {duration}s")
    logger.info("=" * 70)
    logger.info("PIPELINE COMPLETED")
    logger.info("=" * 70)

    return {

        "status": "success",

        "articles_fetched": len(articles),

        "saved": saved_count,

        "duplicates": duplicate_count,

        "failed": failed_count,

        "execution_time": duration
    }

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    run_pipeline()