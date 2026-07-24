# =========================================================
# FILE: core/current_affairs/generator.py
# FINAL UPSC CURRENT AFFAIRS GENERATOR
# =========================================================

from core.current_affairs.processor import (
    process_news_item
)

from core.current_affairs.relevance import (
    detect_category,
    is_upsc_relevant,
    calculate_relevance_score
)


# =========================================================
# GENERATE DAILY CURRENT AFFAIRS
# =========================================================
def get_daily_current_affairs(raw_news):

    """
    Converts raw news feed into UPSC-ready current affairs.
    """

    if not raw_news:
        return []

    processed_news = []
    seen_titles = set()

    for article in raw_news:

        try:

            title = article.get(
                "title",
                ""
            ).strip()

            if not title:
                continue

            # ==========================================
            # DUPLICATE FILTER
            # ==========================================
            title_key = title.lower()

            if title_key in seen_titles:
                continue

            seen_titles.add(title_key)

            # ==========================================
            # DESCRIPTION
            # ==========================================
            description = article.get(
                "description",
                ""
            )

            # ==========================================
            # CATEGORY DETECTION
            # ==========================================
            category = detect_category(
                title,
                description
            )

            # ==========================================
            # UPSC FILTER
            # ==========================================
            if not is_upsc_relevant(
                title,
                category,
                description
            ):
                continue

            # ==========================================
            # PROCESS ARTICLE
            # ==========================================
            processed = process_news_item(
                article
            )

            if not processed:
                continue

            # ==========================================
            # RELEVANCE SCORE
            # ==========================================
            score = calculate_relevance_score(
                title,
                category,
                description
            )

            processed[
                "relevance_score"
            ] = score

            processed_news.append(
                processed
            )

        except Exception as e:

            print(
                "[GENERATOR ERROR]",
                e
            )

            continue

    # ==============================================
    # SORT BY RELEVANCE
    # ==============================================
    processed_news.sort(

        key=lambda x: x.get(
            "relevance_score",
            0
        ),

        reverse=True
    )

    return processed_news


# =========================================================
# TOP CURRENT AFFAIRS
# =========================================================
def get_top_current_affairs(

    raw_news,
    limit=15

):

    news = get_daily_current_affairs(
        raw_news
    )

    return news[:limit]


# =========================================================
# CATEGORY FILTER
# =========================================================
def get_category_news(

    raw_news,
    category

):

    news = get_daily_current_affairs(
        raw_news
    )

    return [

        item

        for item in news

        if item.get(
            "category"
        ) == category
    ]


# =========================================================
# HIGH IMPORTANCE NEWS
# =========================================================
def get_high_importance_news(
    raw_news
):

    news = get_daily_current_affairs(
        raw_news
    )

    return [

        item

        for item in news

        if item.get(
            "importance"
        ) == "High"
    ]


# =========================================================
# API RESPONSE BUILDER
# =========================================================
def build_api_response(

    raw_news,
    limit=20

):

    news = get_top_current_affairs(
        raw_news,
        limit
    )

    return {

        "status": "success",

        "count": len(news),

        "data": news
    }