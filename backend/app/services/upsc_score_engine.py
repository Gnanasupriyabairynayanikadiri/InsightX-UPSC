# =========================================================
# FILE: app/services/upsc_score_engine.py
# UPSC SCORE ENGINE
# =========================================================

print("UPSC SCORE ENGINE LOADED")

CATEGORY_WEIGHT = {

    "International Relations": 20,

    "Polity": 20,

    "Economy": 18,

    "Environment": 18,

    "Science & Technology": 16,

    "Security": 18,

    "Social Issues": 16,

    "Misc": 0
}

SOURCE_WEIGHT = {

    "PIB": 15,

    "Reuters": 12,

    "The Hindu": 12,

    "Indian Express": 10,

    "Business Standard": 10,

    "LiveMint": 8,

    "WHO": 10,

    "UN": 10,

    "RBI": 15,

    "ISRO": 15

}


def calculate_upsc_score(

    category,

    relevance_score,

    source,

    importance,

    india_related,

    government_related

):

    score = 0

    # Category

    score += CATEGORY_WEIGHT.get(category, 5)

    # Relevance

    score += relevance_score * 0.35

    # Trusted source

    score += SOURCE_WEIGHT.get(source, 5)

    # Importance

    if importance == "High":

        score += 15

    elif importance == "Medium":

        score += 8

    else:

        score += 2

    # India focus

    if india_related:

        score += 10

    # Government

    if government_related:

        score += 10

    return round(min(score, 100), 2)