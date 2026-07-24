# =========================================================
# 📁 FILE: core/ca_importance.py
# UPSC CURRENT AFFAIRS IMPORTANCE ENGINE
# =========================================================


# =========================================================
# HIGH IMPORTANCE KEYWORDS
# =========================================================
HIGH_IMPORTANCE = [

    "supreme court",
    "constitution",
    "bill",
    "parliament",
    "g20",
    "un",
    "india china",
    "india us",
    "climate",
    "ai",
    "artificial intelligence",
    "isro",
    "space",
    "budget",
    "economic survey",
    "inflation",
    "rbi",
    "biodiversity",
    "cop summit",
    "semiconductor",
    "digital india",
    "cybersecurity",
    "geopolitics"
]


# =========================================================
# MEDIUM IMPORTANCE KEYWORDS
# =========================================================
MEDIUM_IMPORTANCE = [

    "scheme",
    "policy",
    "education",
    "health",
    "technology",
    "startup",
    "innovation",
    "agriculture",
    "environment",
    "economy",
    "governance",
    "judgment",
    "committee",
    "report",
    "summit",
    "agreement"
]


# =========================================================
# GET IMPORTANCE
# =========================================================
def get_importance(title, category=""):

    text = f"{title} {category}".lower()

    # =====================================================
    # HIGH IMPORTANCE
    # =====================================================
    for keyword in HIGH_IMPORTANCE:

        if keyword in text:

            return "High"

    # =====================================================
    # MEDIUM IMPORTANCE
    # =====================================================
    for keyword in MEDIUM_IMPORTANCE:

        if keyword in text:

            return "Medium"

    # =====================================================
    # DEFAULT
    # =====================================================
    return "Low"


# =========================================================
# IMPORTANCE EMOJI
# =========================================================
def get_importance_emoji(level):

    if level == "High":

        return "🔥"

    elif level == "Medium":

        return "⚡"

    return "📘"


# =========================================================
# IMPORTANCE COLOR
# =========================================================
def get_importance_color(level):

    if level == "High":

        return "red"

    elif level == "Medium":

        return "orange"

    return "green"