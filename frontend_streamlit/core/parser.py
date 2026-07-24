# core/parser.py

import re
from bs4 import BeautifulSoup
from core.logger import log_error


# =========================================================
# 🧹 CLEAN HTML CONTENT
# =========================================================
def clean_html(raw_html):
    try:
        if not raw_html:
            return ""

        soup = BeautifulSoup(raw_html, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # Clean whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    except Exception as e:
        log_error(f"HTML cleaning failed: {e}")
        return ""


# =========================================================
# 📰 PARSE SINGLE ARTICLE
# =========================================================
def parse_article(article):
    """
    Converts raw ingestion data → structured UPSC-ready format
    """

    try:
        title = article.get("title", "").strip()
        content = article.get("content", "")

        clean_content = clean_html(content)

        return {
            "title": title,
            "content": clean_content,
            "source": article.get("source", "Unknown"),
            "published": article.get("published", ""),
            "url": article.get("url", ""),
            "ingested_at": article.get("ingested_at", "")
        }

    except Exception as e:
        log_error(f"Parsing failed: {e}")
        return None


# =========================================================
# 🧾 PARSE BATCH ARTICLES
# =========================================================
def parse_articles(articles):
    parsed = []

    for article in articles:

        cleaned = parse_article(article)

        if cleaned and cleaned["title"]:
            parsed.append(cleaned)

    return parsed


# =========================================================
# 🔍 EXTRACT KEY TERMS (BASIC PRE-AI SIGNAL)
# =========================================================
def extract_keywords(text):
    text = text.lower()

    keywords = []

    patterns = [
        "supreme court", "parliament", "rbi",
        "climate", "economy", "budget",
        "isro", "election", "constitution"
    ]

    for p in patterns:
        if p in text:
            keywords.append(p)

    return list(set(keywords))


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":

    sample = {
        "title": "Supreme Court gives major verdict",
        "content": "<p>The Supreme Court ruled on a key constitutional matter.</p>",
        "source": "The Hindu",
        "published": "2026-05-15"
    }

    result = parse_article(sample)
    print(result)