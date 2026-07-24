# =========================================================
# 📁 FILE: core/map_geo_current_affairs.py
# AI UPSC GEO CURRENT AFFAIRS ENGINE
# =========================================================

import random
from collections import Counter


# =========================================================
# 🌍 CURRENT AFFAIRS DATABASE
# =========================================================
GEO_CURRENT_AFFAIRS = [

    {
        "title":
            "South China Sea Tensions",

        "region":
            "South China Sea",

        "importance":
            "Major global trade route and geopolitical hotspot.",

        "upsc_relevance":
            "International Relations and Indo-Pacific geopolitics.",

        "category":
            "Geopolitics"
    },

    {
        "title":
            "Arctic Sea Route",

        "region":
            "Arctic Region",

        "importance":
            "Melting ice is opening new global trade routes.",

        "upsc_relevance":
            "Climate Change and Shipping Routes.",

        "category":
            "Climate"
    },

    {
        "title":
            "Red Sea Crisis",

        "region":
            "Red Sea",

        "importance":
            "Critical maritime corridor for global trade.",

        "upsc_relevance":
            "Energy Security and World Trade.",

        "category":
            "Geopolitics"
    },

    {
        "title":
            "Himalayan Glacier Melting",

        "region":
            "Himalayas",

        "importance":
            "Threatens river systems and ecology.",

        "upsc_relevance":
            "Environment and Disaster Management.",

        "category":
            "Environment"
    },

    {
        "title":
            "El Niño Impact",

        "region":
            "Pacific Ocean",

        "importance":
            "Affects Indian monsoon and agriculture.",

        "upsc_relevance":
            "Climatology and Agriculture.",

        "category":
            "Climate"
    }
]


# =========================================================
# 🎯 GENERATE RANDOM CURRENT AFFAIR
# =========================================================
def generate_geo_current_affairs():

    return random.choice(
        GEO_CURRENT_AFFAIRS
    )


# =========================================================
# 📚 GET ALL CURRENT AFFAIRS
# =========================================================
def get_all_geo_current_affairs():

    return GEO_CURRENT_AFFAIRS


# =========================================================
# 🔍 SEARCH CURRENT AFFAIRS
# =========================================================
def search_geo_current_affairs(keyword):

    keyword = keyword.lower()

    results = []

    for affair in GEO_CURRENT_AFFAIRS:

        if (

            keyword in affair["title"].lower()

            or keyword in affair["region"].lower()

            or keyword in affair["importance"].lower()

            or keyword in affair["category"].lower()

            or keyword in affair["upsc_relevance"].lower()
        ):

            results.append(affair)

    return results


# =========================================================
# 📂 FILTER BY CATEGORY
# =========================================================
def get_geo_affairs_by_category(category):

    return [

        affair

        for affair in GEO_CURRENT_AFFAIRS

        if affair["category"].lower()
        == category.lower()
    ]


# =========================================================
# 📊 GEO ANALYTICS
# REQUIRED FIX
# =========================================================
def generate_geo_analytics():

    total_affairs = len(
        GEO_CURRENT_AFFAIRS
    )

    categories = [

        affair["category"]

        for affair in GEO_CURRENT_AFFAIRS
    ]

    regions = [

        affair["region"]

        for affair in GEO_CURRENT_AFFAIRS
    ]

    category_count = dict(
        Counter(categories)
    )

    region_count = dict(
        Counter(regions)
    )

    most_common_category = max(
        category_count,
        key=category_count.get
    )

    return {

        "total_affairs":
            total_affairs,

        "categories":
            category_count,

        "regions":
            region_count,

        "most_common_category":
            most_common_category
    }


# =========================================================
# 🌍 GET RANDOM CATEGORY AFFAIR
# =========================================================
def generate_category_affair(category):

    filtered = get_geo_affairs_by_category(
        category
    )

    if filtered:

        return random.choice(filtered)

    return None


# =========================================================
# 🎯 UPSC QUICK FACTS
# =========================================================
def get_geo_quick_facts():

    return [

        "South China Sea handles nearly one-third of global shipping trade.",

        "Hormuz Strait is the world's most important oil chokepoint.",

        "El Niño strongly affects Indian monsoon patterns.",

        "The Arctic region is gaining geopolitical importance due to melting ice.",

        "The Himalayas are called the Water Tower of Asia."
    ]


# =========================================================
# 🧠 UPSC REVISION NOTES
# =========================================================
def get_geo_revision_notes():

    notes = {

        "Geopolitics": [

            "Focus on maritime chokepoints.",
            "Study Indo-Pacific strategy.",
            "Understand global trade routes."
        ],

        "Climate": [

            "Revise El Niño and La Niña.",
            "Study Arctic warming impacts.",
            "Understand climate migration."
        ],

        "Environment": [

            "Study glacier melting.",
            "Understand biodiversity threats.",
            "Revise disaster management basics."
        ]
    }

    return notes