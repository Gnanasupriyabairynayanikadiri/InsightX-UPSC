# =========================================================
# FILE: app/services/ranker.py
# UPSC INTELLIGENCE RANKING ENGINE
# =========================================================


# =========================================================
# UPSC SCORE CALCULATOR
# =========================================================

def calculate_upsc_score(
    title: str,
    category: str,
    importance: str,
    relevance_score: float
):

    category = str(category).strip().title()
    importance = str(importance).strip().title()

    score = 0

    # =====================================================
    # BASE RELEVANCE SCORE
    # =====================================================

    score += float(relevance_score) * 0.5

    # =====================================================
    # CATEGORY WEIGHTS
    # =====================================================

    category_weights = {

        "Polity": 25,

        "Economy": 25,

        "International Relations": 22,

        "Environment": 20,

        "Science & Technology": 18,

        "Security": 18,

        "History": 15,

        "Geography": 15,

        "Current Affairs": 12,

        "General Studies": 10
    }

    score += category_weights.get(
        category,
        10
    )

    # =====================================================
    # IMPORTANCE WEIGHTS
    # =====================================================

    importance_weights = {

        "High": 25,

        "Medium": 15,

        "Low": 5
    }

    score += importance_weights.get(
        importance,
        10
    )

    # =====================================================
    # TITLE BONUS
    # =====================================================

    title_lower = title.lower()

    priority_words = [
        "bill",
        "act",
        "policy",
        "scheme",
        "supreme court",
        "cabinet",
        "parliament",
        "g20",
        "brics",
        "cop",
        "budget",
        "rbi",
        "isro"
    ]

    for word in priority_words:

        if word in title_lower:

            score += 2

    # =====================================================
    # NORMALIZE SCORE
    # =====================================================

    score = round(score, 2)

    return max(
        0,
        min(score, 100)
    )


# =========================================================
# GS PAPER CLASSIFIER
# =========================================================

def classify_gs(
    category: str
):

    category = str(category).strip().title()

    mapping = {

        "Polity": "GS2",

        "International Relations": "GS2",

        "Economy": "GS3",

        "Environment": "GS3",

        "Science & Technology": "GS3",

        "Security": "GS3",

        "History": "GS1",

        "Geography": "GS1",

        "Current Affairs": "GS2"
    }

    return mapping.get(
        category,
        "GS2"
    )


# =========================================================
# UPSC INSIGHT GENERATOR
# =========================================================

def generate_insight(
    title: str,
    category: str
):

    category = str(category).strip().title()

    insights = {

        "Polity":
            (
                "Focus on constitutional provisions, "
                "Supreme Court judgments, governance "
                "issues and institutional reforms."
            ),

        "Economy":
            (
                "Focus on economic impact, fiscal policy, "
                "monetary policy, RBI measures and "
                "government initiatives."
            ),

        "Environment":
            (
                "Focus on biodiversity, conservation, "
                "climate commitments and international "
                "environmental agreements."
            ),

        "Science & Technology":
            (
                "Focus on technological developments, "
                "innovation, digital governance and "
                "their societal impact."
            ),

        "International Relations":
            (
                "Focus on bilateral relations, global "
                "organizations, strategic interests and "
                "India's foreign policy."
            ),

        "History":
            (
                "Focus on historical context, freedom "
                "movement connections and cultural "
                "significance."
            ),

        "Geography":
            (
                "Focus on geographical concepts, mapping, "
                "resources and location relevance."
            ),

        "Current Affairs":
            (
                "Focus on linking the issue with "
                "government schemes, policies, "
                "constitutional provisions and "
                "current developments."
            )
    }

    default_insight = (
        "Focus on conceptual clarity, current affairs "
        "linkage and UPSC relevance."
    )

    return (
        f"This news falls under {category}. "
        f"{insights.get(category, default_insight)} "
        f"Link it with previous year questions, "
        f"government schemes and current developments."
    )