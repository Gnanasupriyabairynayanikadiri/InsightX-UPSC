# =========================================================
# FILE: app/fetchers/news_fetcher.py
# REAL DAILY NEWS FETCHER (DEBUG VERSION)
# =========================================================

import requests

# =========================================================
# NEWS API KEY
# =========================================================
API_KEY = "7901ae84dc304ff5a30af620472ce271"


# =========================================================
# FETCH DAILY NEWS
# =========================================================
def fetch_daily_news():

    try:

        url = (
            "https://newsapi.org/v2/top-headlines"
            "?country=in"
            f"&apiKey={API_KEY}"
        )

        print("\n========== NEWS FETCH START ==========")
        print("REQUEST URL:")
        print(url)

        response = requests.get(
            url,
            timeout=15
        )

        print(f"STATUS CODE = {response.status_code}")

        data = response.json()

        print("\nNEWS API RESPONSE:")
        print(data)

        articles = []

        for item in data.get("articles", []):

            article = {

                "title":
                    item.get("title", ""),

                "description":
                    item.get("description", ""),

                "source":
                    item.get("source", {})
                    .get("name", ""),

                "link":
                    item.get("url", "")
            }

            articles.append(article)

        print(f"\nTOTAL FETCHED = {len(articles)}")

        print("========== NEWS FETCH COMPLETE ==========\n")

        return articles

    except Exception as e:

        print("\n[NEWS FETCH ERROR]")
        print(type(e).__name__)
        print(str(e))

        return []