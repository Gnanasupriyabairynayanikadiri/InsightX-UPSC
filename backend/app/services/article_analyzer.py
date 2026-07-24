# =========================================================
# FILE: app/services/article_analyzer.py
# UPSC ARTICLE ANALYZER
# =========================================================

print("ARTICLE_ANALYZER LOADED")

# =========================================================
# GS PAPER MAPPING
# =========================================================

GS_PAPER = {

    "Polity": "GS2",

    "International Relations": "GS2",

    "Social Issues": "GS2",

    "Economy": "GS3",

    "Environment": "GS3",

    "Science & Technology": "GS3",

    "Security": "GS3",

    "Misc": "GS2"

}

# =========================================================
# ARTICLES THAT SHOULD NEVER ENTER DATABASE
# =========================================================

IGNORE_KEYWORDS = [

    # ----------------------
    # Entertainment
    # ----------------------

    "movie",
    "film",
    "actor",
    "actress",
    "celebrity",
    "music",
    "album",
    "concert",
    "oscar",
    "grammy",
    "box office",
    "netflix",
    "disney",
    "tv show",
    "singer",

    # ----------------------
    # Sports
    # ----------------------

    "football",
    "soccer",
    "cricket",
    "ipl",
    "nba",
    "fifa",
    "olympics",
    "match",
    "goal",
    "tournament",
    "league",
    "player",
    "coach",

    # ----------------------
    # Lifestyle
    # ----------------------

    "recipe",
    "fashion",
    "beauty",
    "shopping",
    "travel",
    "vacation",

    # ----------------------
    # Reviews
    # ----------------------

    "iphone review",
    "camera review",
    "best laptop",
    "top phones",

    # ----------------------
    # Jobs
    # ----------------------

    "job opening",
    "vacancy",
    "president & ceo",
    "chief executive",
    "hiring",

    # ----------------------
    # Finance Noise
    # ----------------------

    "gold price",
    "silver price",
    "stock price",
    "share price",
    "mutual fund",
    "fd rates",
    "fixed deposit",
    "crypto",

    # ----------------------
    # Local News
    # ----------------------

    "weather today",
    "traffic",
    "lottery",

    # ----------------------
    # Crime
    # ----------------------

    "murder",
    "robbery",
    "shooting",
    "kidnapped",
    "rape"

]

# =========================================================
# CATEGORY KEYWORDS
# =========================================================

CATEGORY_KEYWORDS = {

    "Polity": [

        "constitution",
        "constitutional",
        "parliament",
        "lok sabha",
        "rajya sabha",
        "supreme court",
        "high court",
        "judgment",
        "bill",
        "act",
        "ordinance",
        "cabinet",
        "president",
        "governor",
        "election",
        "eci",
        "governance",
        "census",
        "reservation",
        "ministry"

    ],

    "Economy": [

        "economy",
        "economic",
        "budget",
        "rbi",
        "repo",
        "reverse repo",
        "inflation",
        "gdp",
        "bank",
        "banking",
        "gst",
        "tax",
        "trade",
        "fta",
        "free trade",
        "investment",
        "manufacturing",
        "industry",
        "employment",
        "labour",
        "rupee",
        "imf",
        "world bank",
        "Budget",
        "Economic Survey",
        "RBI",
        "SEBI",
        "NITI Aayog",
        "GDP",
        "Inflation",
        "Index",
        "Government Schemes"

    ],

    "Environment": [

        "environment",
        "climate",
        "climate change",
        "global warming",
        "forest",
        "wildlife",
        "biodiversity",
        "species",
        "carbon",
        "net zero",
        "pollution",
        "cop",
        "renewable",
        "renewable energy",
        "solar",
        "wind energy",
        "green mobility",
        "electric vehicle",
        "emissions",
        "ecology",
        "National Parks",
        "Biosphere Reserves",
        "Ramsar Sites",
        "UNFCCC",
        "COP Conferences",
        "IUCN Status",
        "Species in News"

    ],

    "Science & Technology": [

        "technology",
        "artificial intelligence",
        "ai",
        "machine learning",
        "chatgpt",
        "openai",
        "isro",
        "space",
        "satellite",
        "rocket",
        "quantum",
        "semiconductor",
        "chip",
        "cyber",
        "cybersecurity",
        "drone",
        "5g",
        "6g",
        "genome",
        "biotechnology",
        "digital"

    ],

    "International Relations": [

        "india",
        "modi",
        "prime minister",
        "bilateral",
        "strategic partnership",
        "summit",
        "joint statement",
        "foreign",
        "diplomatic",

        "usa",
        "united states",
        "china",
        "russia",
        "ukraine",
        "iran",
        "israel",
        "palestine",
        "gaza",
        "pakistan",
        "bangladesh",
        "new zealand",
        "japan",
        "france",

        "un",
        "united nations",
        "who",
        "unesco",
        "undp",
        "nato",
        "quad",
        "g20",
        "brics",
        "asean"

    ],

    "Security": [

        "terrorism",
        "terrorist",
        "war",
        "army",
        "navy",
        "air force",
        "missile",
        "defence",
        "border",
        "cyber attack"

    ],

    "Social Issues": [

        "education",
        "health",
        "nutrition",
        "poverty",
        "women",
        "child",
        "tribal",
        "caste",
        "welfare"

    ]

}

# =========================================================
# IGNORE ARTICLES
# =========================================================

def should_ignore_article(title, description=""):

    """
    Returns True if article is NOT useful for UPSC.
    """

    text = f"{title} {description}".lower()

    # ---------------------------------------
    # Ignore obvious blacklist
    # ---------------------------------------

    for word in IGNORE_KEYWORDS:

        if word in text:
            return True

    # ---------------------------------------
    # Ignore celebrity names
    # ---------------------------------------

    celebrity_words = [

        "taylor swift",
        "justin bieber",
        "bad bunny",
        "virat kohli",
        "messi",
        "ronaldo",
        "shah rukh",
        "salman khan",
        "deepika",
        "alia bhatt"

    ]

    if any(word in text for word in celebrity_words):

        return True

    # ---------------------------------------
    # Ignore sports scores
    # ---------------------------------------

    sports_terms = [

        "wins",
        "beats",
        "defeats",
        "hat trick",
        "century",
        "goal",
        "semi final",
        "quarter final",
        "final"

    ]

    if any(word in text for word in sports_terms):

        if any(

            sport in text

            for sport in [

                "football",
                "soccer",
                "cricket",
                "ipl",
                "nba",
                "fifa"

            ]

        ):

            return True

    # ---------------------------------------
    # Ignore entertainment awards
    # ---------------------------------------

    if (

        "wins" in text

        and

        any(

            award in text

            for award in [

                "grammy",

                "oscar",

                "filmfare"

            ]

        )

    ):

        return True

    # ---------------------------------------
    # Ignore product launches/reviews
    # ---------------------------------------

    review_words = [

        "review",

        "hands-on",

        "camera",

        "battery",

        "display",

        "launch event"

    ]

    if any(word in text for word in review_words):

        return True

    # ---------------------------------------
    # Ignore job advertisements
    # ---------------------------------------

    job_words = [

        "vacancy",

        "apply now",

        "job opening",

        "career",

        "recruitment"

    ]

    if any(word in text for word in job_words):

        return True

    # ---------------------------------------
    # Ignore local crimes
    # ---------------------------------------

    crime_words = [

        "murder",

        "robbery",

        "kidnap",

        "rape",

        "shooting",

        "stabbing"

    ]

    if any(word in text for word in crime_words):

        return True

    return False

# =========================================================
# DETECT CATEGORY
# =========================================================

def detect_category(title, description=""):

    """
    Detect the best UPSC category for an article.

    Returns:
        Polity
        Economy
        Environment
        Science & Technology
        International Relations
        Security
        Social Issues
        Misc
    """

    text = f"{title} {description}".lower()

    scores = {}

    # ---------------------------------------
    # Calculate keyword score
    # ---------------------------------------

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 1

        scores[category] = score

    # ---------------------------------------
    # Priority Rules
    # ---------------------------------------

    # India + Foreign country
    if "india" in text:

        foreign_words = [

            "china",
            "usa",
            "united states",
            "russia",
            "ukraine",
            "iran",
            "israel",
            "palestine",
            "gaza",
            "pakistan",
            "bangladesh",
            "new zealand",
            "japan",
            "france",
            "g20",
            "quad",
            "brics",
            "asean",
            "united nations"

        ]

        if any(word in text for word in foreign_words):

            return "International Relations"

    # Foreign relations keywords

    if any(

        word in text

        for word in [

            "strategic partnership",

            "joint statement",

            "bilateral",

            "summit",

            "maritime security",

            "foreign minister",

            "diplomatic"

        ]

    ):

        return "International Relations"

    # Supreme Court always Polity

    if any(

        word in text

        for word in [

            "supreme court",

            "high court",

            "judgment",

            "constitutional",

            "constitution"

        ]

    ):

        return "Polity"

    # RBI always Economy

    if any(

        word in text

        for word in [

            "rbi",

            "repo",

            "inflation",

            "budget",

            "gdp"

        ]

    ):

        return "Economy"

    # Climate

    if any(

        word in text

        for word in [

            "climate",

            "carbon",

            "cop",

            "forest",

            "wildlife",

            "renewable"

        ]

    ):

        return "Environment"

    # Science

    if any(

        word in text

        for word in [

            "artificial intelligence",

            "machine learning",

            "chatgpt",

            "openai",

            "isro",

            "space",

            "satellite",

            "quantum",

            "semiconductor",

            "cybersecurity"

        ]

    ):

        return "Science & Technology"

    # Security

    if any(

        word in text

        for word in [

            "terrorism",

            "missile",

            "army",

            "navy",

            "air force",

            "border conflict"

        ]

    ):

        return "Security"

    # ---------------------------------------
    # Highest Score
    # ---------------------------------------

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:

        return "Misc"

    return best_category