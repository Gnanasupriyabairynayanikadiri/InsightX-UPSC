# =========================================================
# FILE: app/services/relevance.py
# UPSC RELEVANCE SCORING ENGINE
# =========================================================

import re

# =========================================================
# CATEGORY BASE SCORES
# =========================================================

CATEGORY_BASE = {

    "Polity": 70,

    "Economy": 68,

    "Environment": 72,

    "Science & Technology": 66,

    "International Relations": 74,

    "Security": 73,

    "Governance": 68,

    "Social Issues": 65,

    "Agriculture": 66,

    "Current Affairs": 55
}

# =========================================================
# HIGH IMPACT UPSC KEYWORDS
# =========================================================

HIGH_IMPACT_KEYWORDS = {

    "constitution",
    "supreme court",
    "high court",
    "judiciary",
    "parliament",
    "bill",
    "act",
    "ordinance",
    "amendment",
    "election commission",
    "finance commission",
    "cag",
    "rbi",
    "inflation",
    "budget",
    "gdp",
    "fiscal",
    "monetary",
    "repo rate",
    "isro",
    "space",
    "quantum",
    "artificial intelligence",
    "semiconductor",
    "climate",
    "cop",
    "biodiversity",
    "forest",
    "carbon",
    "environment",
    "wildlife",
    "g20",
    "brics",
    "quad",
    "india",
    "china",
    "usa",
    "united nations",
    "wto",
    "imf",
    "world bank",
    "geopolitics",
    "diplomacy",
    "cyber security",
    "terrorism",
    "internal security",
    "agriculture",
    "food security",
    "nutrition",
    "health",
    "education",
    "niti aayog",
    "policy",
    "scheme",
    "mission"
}

# =========================================================
# LOW VALUE KEYWORDS
# =========================================================

LOW_VALUE_KEYWORDS = {

    "cricket",

    "football",

    "soccer",

    "match",

    "world cup",

    "ipl",

    "movie",

    "film",

    "actor",

    "actress",

    "celebrity",

    "entertainment",

    "music",

    "youtube",

    "instagram"
}

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# RELEVANCE SCORE
# =========================================================

def calculate_relevance_score(

    title,

    summary="",

    category="Current Affairs"

):

    title = clean_text(title)

    summary = clean_text(summary)

    text = title + " " + summary

    score = CATEGORY_BASE.get(

        category,

        50

    )

    # =====================================================
    # UPSC HIGH VALUE KEYWORDS
    # =====================================================

    for keyword in HIGH_IMPACT_KEYWORDS:

        if keyword in text:

            score += 5

    # =====================================================
    # POLICY TERMS
    # =====================================================

    policy_terms = [

        "policy",

        "scheme",

        "mission",

        "committee",

        "commission",

        "report",

        "framework",

        "guidelines"

    ]

    for word in policy_terms:

        if word in text:

            score += 4

    # =====================================================
    # INTERNATIONAL AGREEMENTS
    # =====================================================

    international_terms = [

        "agreement",

        "treaty",

        "summit",

        "conference",

        "dialogue",

        "strategic partnership"

    ]

    for word in international_terms:

        if word in text:

            score += 3

    # =====================================================
    # ARTICLE LENGTH
    # =====================================================

    if len(summary) > 300:

        score += 5

    elif len(summary) > 150:

        score += 3

    # =====================================================
    # PENALIZE SPORTS / ENTERTAINMENT
    # =====================================================

    for keyword in LOW_VALUE_KEYWORDS:

        if keyword in text:

            score -= 20

    # =====================================================
    # CLAMP SCORE
    # =====================================================

    score = max(

        0,

        min(

            100,

            score

        )

    )

    return round(score, 2)



# =========================================================
# IMPORTANCE LEVEL
# =========================================================

def get_importance(

    title,

    summary="",

    category="Current Affairs"

):

    score = calculate_relevance_score(

        title,

        summary,

        category

    )

    if score >= 80:

        return "High"

    elif score >= 60:

        return "Medium"

    else:

        return "Low"


# =========================================================
# UPSC RELEVANT?
# =========================================================

def is_upsc_relevant(

    title,

    summary="",

    category="Current Affairs"

):

    return (

        calculate_relevance_score(

            title,

            summary,

            category

        ) >= 20
    )