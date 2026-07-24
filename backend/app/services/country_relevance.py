# =========================================================
# COUNTRY RELEVANCE FILTER
# =========================================================

print("COUNTRY RELEVANCE FILTER LOADED")

# ---------------------------------------------------------
# HIGH PRIORITY COUNTRIES
# ---------------------------------------------------------

IMPORTANT_COUNTRIES = [

    "india",
    "indian",

    "china",
    "usa",
    "united states",
    "russia",
    "ukraine",

    "pakistan",
    "bangladesh",
    "nepal",
    "bhutan",
    "sri lanka",
    "maldives",
    "myanmar",

    "iran",
    "israel",
    "palestine",
    "gaza",

    "japan",
    "south korea",
    "north korea",

    "afghanistan",

    "france",
    "germany",
    "uk",

    "new zealand",
    "australia"

]

# ---------------------------------------------------------
# INTERNATIONAL ORGANISATIONS
# ---------------------------------------------------------

GLOBAL_ORGANISATIONS = [

    "un",
    "united nations",
    "security council",

    "who",
    "unesco",
    "undp",

    "wto",

    "world bank",

    "imf",

    "g20",

    "brics",

    "quad",

    "asean",

    "nato",

    "opec"

]

# ---------------------------------------------------------
# GLOBAL ISSUES
# ---------------------------------------------------------

GLOBAL_ISSUES = [

    "climate change",

    "global warming",

    "pandemic",

    "terrorism",

    "cybersecurity",

    "artificial intelligence",

    "semiconductor",

    "energy transition",

    "critical minerals",

    "maritime security",

    "indo-pacific",

    "south china sea"

]

# ---------------------------------------------------------
# REJECT COUNTRIES
# ---------------------------------------------------------

LOW_PRIORITY = [

    "nigeria",

    "ireland",

    "liberia",

    "venezuela",

    "ecuador",

    "argentina",

    "peru",

    "colombia",

    "mexico",

    "chile",

    "paraguay"

]

# =========================================================
# MAIN FUNCTION
# =========================================================

def is_country_relevant(title, description=""):

    text = f"{title} {description}".lower()

    # India always accepted

    if "india" in text:

        return True

    # Important country

    for country in IMPORTANT_COUNTRIES:

        if country in text:

            return True

    # Global organisations

    for org in GLOBAL_ORGANISATIONS:

        if org in text:

            return True

    # Global issue

    for issue in GLOBAL_ISSUES:

        if issue in text:

            return True

    # Low priority country

    for country in LOW_PRIORITY:

        if country in text:

            return False

    return False