# =========================================================
# FILE: app/services/relevance_filter.py
# UPSC RELEVANCE FILTER
# =========================================================

print("RELEVANCE FILTER LOADED")

from app.services.country_relevance import is_country_relevant

# =========================================================
# IMPORTANT UPSC KEYWORDS
# =========================================================

UPSC_KEYWORDS = [

    # Polity
    "constitution",
    "parliament",
    "supreme court",
    "high court",
    "judgment",
    "bill",
    "act",
    "governance",
    "cabinet",
    "governor",
    "president",
    "election",

    # Economy
    "economy",
    "economic",
    "inflation",
    "gdp",
    "budget",
    "rbi",
    "repo",
    "bank",
    "banking",
    "trade",
    "fta",
    "export",
    "import",
    "investment",
    "manufacturing",
    "employment",
    "gst",
    "tax",

    # Environment
    "climate",
    "climate change",
    "forest",
    "wildlife",
    "pollution",
    "biodiversity",
    "renewable",
    "net zero",
    "green energy",

    # Science & Tech
    "technology",
    "artificial intelligence",
    "ai",
    "machine learning",
    "cyber",
    "cybersecurity",
    "space",
    "satellite",
    "isro",
    "rocket",
    "quantum",
    "semiconductor",
    "drone",
    "genome",
    "biotechnology",

    # International Relations
    "bilateral",
    "strategic partnership",
    "summit",
    "foreign policy",
    "diplomatic",
    "un",
    "united nations",
    "g20",
    "brics",
    "quad",
    "asean",
    "nato",
    "who",
    "wto",
    "imf",
    "world bank",

    # Security
    "terrorism",
    "defence",
    "security",
    "missile",
    "army",
    "navy",
    "air force",
    "border",
    "war",

    # Social
    "education",
    "health",
    "nutrition",
    "poverty",
    "women",
    "child",
    "tribal",
    "reservation"
]

# =========================================================
# ALWAYS IGNORE
# =========================================================

BLACKLIST = [

    # Entertainment
    "movie",
    "film",
    "actor",
    "actress",
    "celebrity",
    "music",
    "album",
    "concert",
    "grammy",
    "oscar",
    "netflix",

    # Sports
    "cricket",
    "football",
    "soccer",
    "ipl",
    "fifa",
    "nba",
    "match",
    "goal",
    "player",
    "coach",

    # Lifestyle
    "fashion",
    "beauty",
    "shopping",
    "recipe",
    "travel",
    "vacation",

    # Promotions
    "amazon sale",
    "discount",
    "coupon",
    "iphone review",
    "bestseller",

    # Finance noise
    "gold price",
    "silver price",
    "share price",
    "stock price",
    "crypto",
    "bitcoin"
]

# =========================================================
# MAIN FILTER
# =========================================================

def is_upsc_relevant(title, description="", source=""):

    text = f"{title} {description}".lower()

    # -----------------------------------------------------
    # 1. Entertainment/Sports filter
    # -----------------------------------------------------

    for word in BLACKLIST:

        if word in text:

            return False, f"Ignored keyword: {word}"

    # -----------------------------------------------------
    # 2. India articles
    # -----------------------------------------------------

    if "india" in text or "indian" in text:

        return True, "India related"

    # -----------------------------------------------------
    # 3. Country relevance
    # -----------------------------------------------------

    if is_country_relevant(title, description):

        return True, "Important country"

    # -----------------------------------------------------
    # 4. UPSC keywords
    # -----------------------------------------------------

    for word in UPSC_KEYWORDS:

        if word in text:

            return True, f"Matched keyword: {word}"

    # -----------------------------------------------------
    # 5. Government sources
    # -----------------------------------------------------

    source = source.lower()

    if any(x in source for x in [

        "pib",
        "press information bureau",
        "prs",
        "isro",
        "rbi",
        "mea",
        "mha",
        "mospi",
        "government"

    ]):

        return True, "Government source"

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    return False, "Not UPSC relevant"