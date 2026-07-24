# core/dedup.py

import re
from difflib import SequenceMatcher
from core.logger import log_info


# =========================================================
# 🧹 TEXT NORMALIZATION
# =========================================================
def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


# =========================================================
# 📊 SIMILARITY SCORE
# =========================================================
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


# =========================================================
# 🔍 CHECK IF DUPLICATE
# =========================================================
def is_duplicate(new_item, existing_items, threshold=0.82):
    """
    Returns True if similar article already exists
    """

    new_text = normalize(new_item.get("title", ""))

    for item in existing_items:
        existing_text = normalize(item.get("title", ""))

        score = similarity(new_text, existing_text)

        if score >= threshold:
            return True

    return False


# =========================================================
# 🧠 UPSC TOPIC CLUSTER DUPLICATION (ADVANCED RULE)
# =========================================================
def is_topic_duplicate(new_item, existing_items):

    new_title = normalize(new_item.get("title", ""))

    keywords = [
        "rbi", "supreme court", "parliament",
        "budget", "climate", "isro", "inflation",
        "election", "constitution"
    ]

    new_hits = [k for k in keywords if k in new_title]

    for item in existing_items:

        old_title = normalize(item.get("title", ""))
        old_hits = [k for k in keywords if k in old_title]

        # if same UPSC topic cluster → treat as duplicate
        if set(new_hits) & set(old_hits):
            return True

    return False


# =========================================================
# 🧠 SMART FILTER (MAIN FUNCTION)
# =========================================================
def deduplicate_articles(new_articles, existing_articles):
    """
    Removes duplicates + topic overlap
    """

    filtered = []

    for article in new_articles:

        if not article.get("title"):
            continue

        # Rule 1: exact similarity check
        if is_duplicate(article, existing_articles):
            log_info(f"Duplicate removed: {article['title']}")
            continue

        # Rule 2: UPSC topic overlap check
        if is_topic_duplicate(article, existing_articles):
            log_info(f"Topic duplicate removed: {article['title']}")
            continue

        filtered.append(article)

    return filtered


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":

    old = [
        {"title": "RBI keeps repo rate unchanged amid inflation concerns"}
    ]

    new = [
        {"title": "RBI holds repo rate steady due to inflation pressure"},
        {"title": "Supreme Court delivers verdict on constitutional issue"},
    ]

    result = deduplicate_articles(new, old)

    print("Filtered:", result)