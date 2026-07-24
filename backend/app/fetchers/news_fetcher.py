# =========================================================
# FILE: app/fetchers/news_fetcher.py
# GOOGLE NEWS RSS FETCHER
# =========================================================

import re
import html
import feedparser

print("GOOGLE NEWS FETCHER LOADED")

# =========================================================
# GOOGLE NEWS RSS
# =========================================================

RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=India+OR+government+OR+parliament+OR+constitution+"
    "OR+supreme+court+OR+economy+OR+environment+"
    "OR+ISRO+OR+science+OR+technology+OR+international+relations"
    "&hl=en-IN&gl=IN&ceid=IN:en"
)

# =========================================================
# CLEAN HTML
# =========================================================

def clean_html(text):

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(r"<.*?>", "", text)

    text = text.replace("&nbsp;", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# CLEAN TITLE
# =========================================================

def clean_title(title):

    if not title:
        return ""

    title = html.unescape(title)

    title = re.sub(
        r"\s*-\s*(The Times of India|The Hindu|Hindustan Times|NDTV|Indian Express|Economic Times|Business Standard|LiveMint|Reuters|BBC News)$",
        "",
        title,
        flags=re.IGNORECASE,
    )

    return title.strip()


# =========================================================
# EXTRACT SOURCE
# =========================================================

def extract_source(title):

    if " - " in title:

        return title.split(" - ")[-1].strip()

    return "Google News"


# =========================================================
# FETCH DAILY NEWS
# =========================================================

def fetch_daily_news():

    print("\n===================================")
    print("FETCHING GOOGLE NEWS RSS")
    print("===================================")

    feed = feedparser.parse(RSS_URL)

    print(f"RSS Entries : {len(feed.entries)}")

    news_items = []

    seen_links = set()

    for entry in feed.entries:

        title = clean_title(entry.get("title", ""))

        description = clean_html(
            entry.get("summary", "")
        )

        source = extract_source(
            entry.get("title", "")
        )

        link = entry.get("link", "")

        if not title:
            continue

        if link in seen_links:
            continue

        seen_links.add(link)

        news_items.append({

            "title": title,

            "description": description,

            "source": source,

            "link": link

        })

    print(f"Clean Articles : {len(news_items)}")

    print("===================================\n")

    return news_items