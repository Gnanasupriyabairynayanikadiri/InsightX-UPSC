# =========================================================
# FILE: core/current_affairs/pyq_mapper.py
# FINAL UPSC PYQ MAPPING ENGINE
# =========================================================


# =========================================================
# STATIC PYQ DATABASE
# =========================================================

PYQ_DATABASE = {

    "Polity": [

        {
            "year": 2023,
            "exam": "Prelims",
            "question":
                "With reference to the Indian Constitution, discuss constitutional amendments."
        },

        {
            "year": 2021,
            "exam": "GS Paper II",
            "question":
                "Examine the role of judicial review in Indian democracy."
        },

        {
            "year": 2020,
            "exam": "GS Paper II",
            "question":
                "Discuss issues related to federalism in India."
        }
    ],

    # =====================================================
    # ECONOMY
    # =====================================================

    "Economy": [

        {
            "year": 2023,
            "exam": "Prelims",
            "question":
                "Questions related to inflation and monetary policy."
        },

        {
            "year": 2022,
            "exam": "GS Paper III",
            "question":
                "Discuss RBI's role in inflation control."
        },

        {
            "year": 2021,
            "exam": "GS Paper III",
            "question":
                "Examine challenges to economic growth."
        }
    ],

    # =====================================================
    # ENVIRONMENT
    # =====================================================

    "Environment": [

        {
            "year": 2023,
            "exam": "Prelims",
            "question":
                "Questions related to climate change and biodiversity."
        },

        {
            "year": 2022,
            "exam": "GS Paper III",
            "question":
                "Discuss biodiversity conservation in India."
        },

        {
            "year": 2021,
            "exam": "GS Paper III",
            "question":
                "Examine environmental governance challenges."
        }
    ],

    # =====================================================
    # SCIENCE & TECHNOLOGY
    # =====================================================

    "Science & Technology": [

        {
            "year": 2023,
            "exam": "Prelims",
            "question":
                "Questions related to Artificial Intelligence."
        },

        {
            "year": 2022,
            "exam": "GS Paper III",
            "question":
                "Discuss emerging technologies and governance."
        },

        {
            "year": 2021,
            "exam": "GS Paper III",
            "question":
                "Examine India's innovation ecosystem."
        }
    ],

    # =====================================================
    # INTERNATIONAL RELATIONS
    # =====================================================

    "International Relations": [

        {
            "year": 2023,
            "exam": "GS Paper II",
            "question":
                "Discuss India's role in global institutions."
        },

        {
            "year": 2022,
            "exam": "GS Paper II",
            "question":
                "Examine India's foreign policy challenges."
        },

        {
            "year": 2021,
            "exam": "Prelims",
            "question":
                "Questions related to international organizations."
        }
    ],

    # =====================================================
    # SOCIAL ISSUES
    # =====================================================

    "Social Issues": [

        {
            "year": 2023,
            "exam": "GS Paper II",
            "question":
                "Discuss challenges in healthcare delivery."
        },

        {
            "year": 2022,
            "exam": "GS Paper II",
            "question":
                "Examine issues related to education reforms."
        }
    ]
}


# =========================================================
# CATEGORY PYQ FETCHER
# =========================================================

def map_pyq_references(title, category):

    """
    Returns relevant PYQs for a category.
    """

    return PYQ_DATABASE.get(category, [])


# =========================================================
# TOP PYQ
# =========================================================

def get_top_pyq(title, category):

    pyqs = map_pyq_references(
        title,
        category
    )

    if not pyqs:
        return None

    return pyqs[0]


# =========================================================
# PYQ COUNT
# =========================================================

def get_pyq_count(category):

    return len(
        PYQ_DATABASE.get(category, [])
    )


# =========================================================
# UPSC RELEVANCE MESSAGE
# =========================================================

def generate_pyq_insight(title, category):

    count = get_pyq_count(category)

    if count == 0:

        return (
            "No direct PYQ mapping available."
        )

    return (
        f"This topic is linked with "
        f"{count} UPSC PYQs from previous years."
    )


# =========================================================
# COMPATIBILITY ALIAS
# =========================================================

def get_pyq_references(title, category):

    return map_pyq_references(
        title,
        category
    )