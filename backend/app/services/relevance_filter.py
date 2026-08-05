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

def is_upsc_relevant(title, description, source):
    text = f"{title} {description} {source}".lower()

    # Strong India-UPSC keywords
    strong_keywords = [
        "india", "indian", "new delhi", "parliament", "supreme court",
        "cabinet", "ministry", "policy", "scheme", "rbi", "isro", "upsc",
        "brics", "asean", "quad", "g20", "united nations", "bangladesh",
        "pakistan", "china", "usa", "trade agreement", "fta", "ai summit"
    ]

    # Ignore generic international opinion/editorial content
    ignore_keywords = [
        "opinion", "editorial", "research article", "vision of", "future trajectory",
        "inside the games", "council on foreign relations", "parliament magazine",
        "commonwealth round table", "9dashline", "e-international relations"
    ]

    if any(k in text for k in ignore_keywords):
        return False, "Generic opinion/editorial article"

    if any(k in text for k in strong_keywords):
        return True, "Contains strong UPSC-relevant India keywords"

    return False, "Not sufficiently India-UPSC relevant"