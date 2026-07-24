# =========================================================
# FILE: core/current_affairs/revision.py
# UPSC REVISION ENGINE
# =========================================================

from datetime import datetime


# =========================================================
# STATIC REVISION DATABASE
# =========================================================

REVISION_DATABASE = {

    "Polity": [
        "Fundamental Rights",
        "Directive Principles",
        "Parliament",
        "Judiciary",
        "Constitutional Bodies",
        "Federalism"
    ],

    "Economy": [
        "Inflation",
        "GDP",
        "Fiscal Deficit",
        "Monetary Policy",
        "Banking",
        "Budget"
    ],

    "Environment": [
        "Climate Change",
        "Biodiversity",
        "Protected Areas",
        "Pollution",
        "International Conventions"
    ],

    "Science & Technology": [
        "Artificial Intelligence",
        "Semiconductors",
        "Quantum Computing",
        "ISRO Missions",
        "Cyber Security"
    ],

    "International Relations": [
        "India-US Relations",
        "India-China Relations",
        "BRICS",
        "G20",
        "United Nations"
    ],

    "Social Issues": [
        "Education",
        "Healthcare",
        "Nutrition",
        "Women Empowerment",
        "Poverty"
    ]
}


# =========================================================
# MOTIVATION
# =========================================================

MOTIVATION_QUOTES = [

    "Consistency creates UPSC rankers.",

    "Revision converts knowledge into retention.",

    "Small daily progress creates big results.",

    "Discipline beats motivation.",

    "Every revision cycle increases recall."
]


# =========================================================
# SUBJECT REVISION
# =========================================================

def get_subject_revision(subject, limit=5):

    topics = REVISION_DATABASE.get(subject, [])

    return topics[:limit]


# =========================================================
# WEAK AREA REVISION
# =========================================================

def get_weak_area_revision(user_progress):

    """
    Example:

    {
        "Polity": 40,
        "Economy": 80,
        "Environment": 35
    }
    """

    revision = []

    for subject, score in user_progress.items():

        if score < 50:

            revision.append({

                "subject": subject,

                "topics":
                    get_subject_revision(
                        subject,
                        3
                    )
            })

    return revision


# =========================================================
# CURRENT AFFAIRS REVISION
# =========================================================

def generate_current_affairs_revision(news_items):

    revision_points = []

    for item in news_items:

        title = item.get("title", "")

        category = item.get(
            "category",
            "General Studies"
        )

        revision_points.append({

            "title": title,

            "category": category,

            "revision_focus":

                f"Revise static concepts related to {category}."
        })

    return revision_points


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

def analyze_current_affairs(news_items):

    stats = {}

    for item in news_items:

        category = item.get(
            "category",
            "General Studies"
        )

        stats[category] = (
            stats.get(category, 0) + 1
        )

    return stats


# =========================================================
# AI INSIGHTS
# =========================================================

def generate_ai_insights(news_items):

    stats = analyze_current_affairs(
        news_items
    )

    if not stats:

        return [
            "No current affairs available."
        ]

    top_category = max(
        stats,
        key=stats.get
    )

    insights = [

        f"Today's current affairs were dominated by {top_category}.",

        f"Revise static portions linked with {top_category}.",

        "Link current affairs with Mains answer writing.",

        "Use current examples in GS answers."
    ]

    return insights


# =========================================================
# DAILY MOTIVATION
# =========================================================

def get_daily_motivation():

    day = datetime.now().day

    index = day % len(
        MOTIVATION_QUOTES
    )

    return MOTIVATION_QUOTES[index]


# =========================================================
# DAILY REVISION PLAN
# =========================================================

def generate_daily_revision_plan(

    user_progress,
    news_items
):

    return {

        "date":
            str(datetime.now().date()),

        "weak_area_revision":
            get_weak_area_revision(
                user_progress
            ),

        "current_affairs_revision":
            generate_current_affairs_revision(
                news_items
            ),

        "insights":
            generate_ai_insights(
                news_items
            ),

        "motivation":
            get_daily_motivation()
    }


# =========================================================
# SPACED REPETITION
# =========================================================

def get_revision_cycles():

    return {

        "Day 1":
            "Initial Revision",

        "Day 3":
            "Concept Reinforcement",

        "Day 7":
            "Retention Testing",

        "Day 15":
            "Advanced Revision",

        "Day 30":
            "Full Consolidation"
    }