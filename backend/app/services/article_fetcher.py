# =========================================================
# FILE: app/services/current_affairs_fetcher.py
# UPSC CURRENT AFFAIRS FETCHER
# =========================================================

import requests
from datetime import datetime, timedelta

NEWS_API_KEY = "9feea95ac11149e1bb49f4f6e5c34915"


def fetch_articles():

    from_date = (
        datetime.now() - timedelta(days=2)
    ).strftime("%Y-%m-%d")

    url = (
        "https://newsapi.org/v2/everything?"
        f"domains=thehindu.com,"
        f"indianexpress.com,"
        f"business-standard.com,"
        f"livemint.com,"
        f"downtoearth.org.in&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"from={from_date}&"
        f"pageSize=50&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        print("NewsAPI Error:", e)

        return []

    articles = []

    for item in data.get(
        "articles",
        []
    ):

        title = item.get(
            "title",
            ""
        )

        description = item.get(
            "description",
            ""
        )

        content = item.get(
            "content",
            ""
        )

        articles.append({

            "article_date":
                item.get(
                    "publishedAt",
                    datetime.now().strftime(
                        "%Y-%m-%d"
                    )
                ),

            "title":
                title,

            "category":
                detect_category(
                    title,
                    description
                ),

            "source_name":
                item.get(
                    "source",
                    {}
                ).get(
                    "name",
                    "Unknown"
                ),

            "article_url":
                item.get(
                    "url",
                    ""
                ),

            "summary":
                description,

            "full_analysis":
                content,

            "relevance_score":
                70,

            "upsc_score":
                70,

            "importance_level":
                "Medium"
        })

    return articles


# =========================================================
# CATEGORY DETECTION
# =========================================================

def detect_category(
    title,
    description
):

    text = (
        f"{title} {description}"
    ).lower()

    if any(
        k in text
        for k in [
            "parliament",
            "constitution",
            "supreme court",
            "election",
            "bill"
        ]
    ):
        return "Polity"

    elif any(
        k in text
        for k in [
            "gdp",
            "economy",
            "inflation",
            "rbi",
            "budget"
        ]
    ):
        return "Economy"

    elif any(
        k in text
        for k in [
            "climate",
            "forest",
            "wildlife",
            "environment",
            "biodiversity"
        ]
    ):
        return "Environment"

    elif any(
        k in text
        for k in [
            "india",
            "china",
            "usa",
            "un",
            "g20",
            "nato",
            "iran"
        ]
    ):
        return "International Relations"

    elif any(
        k in text
        for k in [
            "ai",
            "technology",
            "space",
            "satellite",
            "science"
        ]
    ):
        return "Science & Technology"

    return "Current Affairs"