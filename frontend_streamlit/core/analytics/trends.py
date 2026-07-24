# =========================================================
# 📁 FILE: core/analytics/trends.py
# UPSC CURRENT AFFAIRS ANALYTICS ENGINE
# =========================================================

from collections import Counter

from core.current_affairs.storage import (
    get_monthly_current_affairs
)


# =========================================================
# CATEGORY DISTRIBUTION
# =========================================================
def get_category_distribution():

    news = get_monthly_current_affairs()

    categories = [

        item.get("category", "General")

        for item in news
    ]

    return dict(Counter(categories))


# =========================================================
# IMPORTANCE DISTRIBUTION
# =========================================================
def get_importance_distribution():

    news = get_monthly_current_affairs()

    importance = [

        item.get("importance", "Medium")

        for item in news
    ]

    return dict(Counter(importance))


# =========================================================
# MOST REPEATED TOPICS
# =========================================================
def get_trending_keywords(limit=10):

    news = get_monthly_current_affairs()

    keywords = []

    important_words = [

        "India",
        "government",
        "policy",
        "scheme",
        "economy",
        "climate",
        "AI",
        "China",
        "RBI",
        "Supreme Court",
        "Parliament"
    ]

    for item in news:

        title = item.get("title", "")

        for word in important_words:

            if word.lower() in title.lower():

                keywords.append(word)

    return Counter(keywords).most_common(limit)


# =========================================================
# HIGH IMPORTANCE NEWS
# =========================================================
def get_high_priority_news():

    news = get_monthly_current_affairs()

    return [

        item for item in news

        if item.get("importance") == "High"
    ]


# =========================================================
# UPSC ANALYTICS SUMMARY
# =========================================================
def generate_monthly_analysis():

    categories = get_category_distribution()

    importance = get_importance_distribution()

    trends = get_trending_keywords()

    return {

        "categories": categories,

        "importance": importance,

        "trending_topics": trends
    }