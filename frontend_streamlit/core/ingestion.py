# core/ingestion.py

import requests
import feedparser
from datetime import datetime
from core.logger import log_error, log_info


# =========================================================
# 📰 SOURCE CONFIG
# =========================================================
RSS_FEEDS = {
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "PIB": "https://pib.gov.in/rsssite/rssfeed.aspx?feed=EnglishRSS",
    "Indian Express": "https://indianexpress.com/section/india/feed/"
}


# =========================================================
# 🔄 FETCH FROM RSS
# =========================================================
def fetch_rss(url, source_name):
    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.get("title", "").strip(),
                "content": entry.get("summary", "").strip(),
                "source": source_name,
                "published": entry.get("published", ""),
                "url": entry.get("link", ""),
                "ingested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return articles

    except Exception as e:
        log_error(f"RSS fetch failed for {source_name}: {e}")
        return []


# =========================================================
# 🌐 FETCH ALL SOURCES
# =========================================================
def fetch_all_news():
    all_news = []

    for source_name, url in RSS_FEEDS.items():
        log_info(f"Fetching from {source_name}")
        data = fetch_rss(url, source_name)
        all_news.extend(data)

    return all_news


# =========================================================
# 🧹 BASIC CLEANING
# =========================================================
def clean_article(article):
    return {
        "text": article.get("title", ""),
        "content": article.get("content", ""),
        "source": article.get("source", "Unknown"),
        "published": article.get("published", ""),
        "url": article.get("url", ""),
        "ingested_at": article.get("ingested_at")
    }


# =========================================================
# 📦 MAIN INGESTION PIPELINE
# =========================================================
def ingest_news():
    raw_news = fetch_all_news()

    cleaned = []

    for article in raw_news:
        if not article.get("title"):
            continue

        cleaned.append(clean_article(article))

    return cleaned


# =========================================================
# 🧪 TEST RUN
# =========================================================
if __name__ == "__main__":
    news = ingest_news()
    print(f"Fetched {len(news)} articles")

    for n in news[:3]:
        print(n["text"], n["source"])