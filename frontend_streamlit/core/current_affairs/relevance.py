# =========================================================
# FILE: core/current_affairs/relevance.py
# FINAL UPSC RELEVANCE ENGINE
# =========================================================

import re


# =========================================================
# CATEGORY KEYWORDS
# =========================================================

CATEGORY_KEYWORDS = {

    "Polity": [
        "supreme court",
        "high court",
        "constitution",
        "constitutional",
        "parliament",
        "bill",
        "ordinance",
        "governor",
        "president",
        "election",
        "judiciary",
        "tribunal",
        "federalism"
    ],

    "Economy": [
        "rbi",
        "inflation",
        "repo rate",
        "gdp",
        "budget",
        "economic survey",
        "fiscal deficit",
        "banking",
        "economy",
        "tax",
        "startup",
        "investment",
        "manufacturing",
        "semiconductor"
    ],

    "Environment": [
        "climate",
        "climate change",
        "biodiversity",
        "wetland",
        "forest",
        "pollution",
        "renewable",
        "wildlife",
        "carbon",
        "conservation",
        "cop"
    ],

    "Science & Technology": [
        "ai",
        "artificial intelligence",
        "quantum",
        "isro",
        "satellite",
        "space",
        "cyber security",
        "data protection",
        "technology",
        "innovation",
        "semiconductor"
    ],

    "International Relations": [
        "g20",
        "brics",
        "quad",
        "indo-pacific",
        "united nations",
        "unsc",
        "china",
        "russia",
        "usa",
        "strategic partnership",
        "diplomatic",
        "maritime"
    ],

    "Social Issues": [
        "education",
        "health",
        "poverty",
        "nutrition",
        "employment",
        "women",
        "child",
        "healthcare"
    ]
}


# =========================================================
# HIGH VALUE UPSC KEYWORDS
# =========================================================

HIGH_VALUE_TOPICS = {

    "supreme court": 20,
    "constitution": 20,
    "parliament": 15,
    "bill": 12,

    "rbi": 20,
    "inflation": 18,
    "budget": 20,
    "gdp": 15,

    "climate": 18,
    "biodiversity": 15,
    "pollution": 12,

    "g20": 18,
    "brics": 15,
    "indo-pacific": 18,

    "ai": 18,
    "artificial intelligence": 20,
    "isro": 20,
    "quantum": 15
}


# =========================================================
# LOW VALUE TOPICS
# =========================================================

LOW_VALUE_TOPICS = {

    "celebrity": -50,
    "movie": -50,
    "actor": -40,
    "actress": -40,

    "cricket": -50,
    "ipl": -50,
    "football": -40,
    "match": -30,

    "entertainment": -50,
    "viral": -50,
    "youtube": -40,
    "instagram": -40,

    "fashion": -40,
    "box office": -50
}


# =========================================================
# CATEGORY BONUS
# =========================================================

CATEGORY_BONUS = {

    "Polity": 20,
    "Economy": 20,
    "Environment": 18,
    "Science & Technology": 18,
    "International Relations": 18,
    "Social Issues": 12,
    "General Studies": 5
}


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s\-]",
        " ",
        text
    )

    return text


# =========================================================
# CATEGORY DETECTOR
# =========================================================

def detect_category(
    title,
    description=""
):

    text = clean_text(
        f"{title} {description}"
    )

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:

        return "General Studies"

    return best_category


# =========================================================
# RELEVANCE SCORE
# =========================================================

def calculate_relevance_score(

    title,
    category="General Studies",
    description=""

):

    text = clean_text(
        f"{title} {description}"
    )

    score = 40

    # ======================================
    # HIGH VALUE BOOST
    # ======================================

    for keyword, value in HIGH_VALUE_TOPICS.items():

        if keyword in text:
            score += value

    # ======================================
    # LOW VALUE PENALTY
    # ======================================

    for keyword, penalty in LOW_VALUE_TOPICS.items():

        if keyword in text:
            score += penalty

    # ======================================
    # CATEGORY BONUS
    # ======================================

    score += CATEGORY_BONUS.get(
        category,
        0
    )

    # ======================================
    # LONG TITLE BONUS
    # ======================================

    if len(title.split()) >= 5:
        score += 5

    # ======================================
    # LIMIT SCORE
    # ======================================

    score = max(
        0,
        min(score, 100)
    )

    return score


# =========================================================
# IMPORTANCE
# =========================================================

def get_importance(

    title,
    category="General Studies",
    description=""

):

    score = calculate_relevance_score(

        title,
        category,
        description
    )

    if score >= 80:
        return "High"

    elif score >= 60:
        return "Medium"

    return "Low"


# =========================================================
# RELEVANCE LABEL
# =========================================================

def get_relevance_label(score):

    if score >= 80:
        return "Very High"

    elif score >= 60:
        return "High"

    elif score >= 40:
        return "Medium"

    return "Low"


# =========================================================
# UPSC FILTER
# =========================================================

def is_upsc_relevant(

    title,
    category="General Studies",
    description=""

):

    score = calculate_relevance_score(

        title,
        category,
        description
    )

    return score >= 40