# =========================================================
# FILE: core/current_affairs/editorial_engine.py
# FINAL UPSC EDITORIAL ENGINE
# =========================================================

import re


# =========================================================
# GS PAPER MAPPING
# =========================================================

CATEGORY_ANALYSIS = {

    "Polity": {
        "gs_paper": "GS Paper II"
    },

    "Economy": {
        "gs_paper": "GS Paper III"
    },

    "Environment": {
        "gs_paper": "GS Paper III"
    },

    "Science & Technology": {
        "gs_paper": "GS Paper III"
    },

    "International Relations": {
        "gs_paper": "GS Paper II"
    },

    "Social Issues": {
        "gs_paper": "GS Paper II"
    },

    "General Studies": {
        "gs_paper": "General Studies"
    }
}


# =========================================================
# CLEAN TITLE
# =========================================================

def clean_title(title):

    if not title:
        return ""

    title = str(title)

    title = title.replace(
        ":",
        " "
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


# =========================================================
# GS PAPER DETECTOR
# =========================================================

def detect_gs_paper(category):

    return CATEGORY_ANALYSIS.get(

        category,

        {
            "gs_paper":
                "General Studies"
        }

    ).get("gs_paper")


# =========================================================
# BACKGROUND
# =========================================================

def generate_background(

    title,
    category

):

    title = clean_title(title)

    templates = {

        "Polity":
            f"The issue of '{title}' has implications for constitutional governance, institutions and public policy.",

        "Economy":
            f"The issue of '{title}' is important for understanding economic growth, fiscal management and macroeconomic stability.",

        "Environment":
            f"The issue of '{title}' is relevant for environmental sustainability, biodiversity conservation and climate action.",

        "Science & Technology":
            f"The issue of '{title}' highlights emerging technological developments and their policy implications.",

        "International Relations":
            f"The issue of '{title}' is important for India's foreign policy, diplomacy and strategic interests.",

        "Social Issues":
            f"The issue of '{title}' is linked with welfare, inclusion and socio-economic development."
    }

    return templates.get(

        category,

        f"The issue of '{title}' has significance for governance and public policy."
    )


# =========================================================
# SIGNIFICANCE
# =========================================================

def generate_significance(

    title,
    category

):

    common = [

        "Important for UPSC Prelims",

        "Useful for GS Mains answer writing",

        "Relevant for policy understanding"
    ]

    category_specific = {

        "Polity": [
            "Governance relevance",
            "Constitutional implications"
        ],

        "Economy": [
            "Economic implications",
            "Fiscal and monetary relevance"
        ],

        "Environment": [
            "Climate relevance",
            "Environmental sustainability"
        ],

        "Science & Technology": [
            "Technological innovation",
            "Strategic significance"
        ],

        "International Relations": [
            "Foreign policy relevance",
            "Geopolitical significance"
        ],

        "Social Issues": [
            "Social development relevance",
            "Public welfare implications"
        ]
    }

    return common + category_specific.get(
        category,
        []
    )


# =========================================================
# MAINS QUESTION
# =========================================================

def generate_mains_question(

    title,
    category

):

    title = clean_title(title)

    templates = {

        "Polity":
            f"Discuss the constitutional and governance implications of {title}.",

        "Economy":
            f"Analyze the economic significance of {title}.",

        "Environment":
            f"Examine the environmental implications of {title}.",

        "Science & Technology":
            f"Discuss the role of science and technology in relation to {title}.",

        "International Relations":
            f"Evaluate the impact of {title} on India's foreign policy and strategic interests.",

        "Social Issues":
            f"Discuss the socio-economic implications of {title}."
    }

    return templates.get(

        category,

        f"Discuss the significance of {title}."
    )


# =========================================================
# ANSWER FRAMEWORK
# =========================================================

def generate_answer_framework(

    title,
    category

):

    return {

        "introduction":

            f"Briefly introduce {title}.",

        "body": [

            "Background and context",

            "Key developments",

            "Challenges involved",

            "Implications",

            "Government initiatives",

            "Way forward"
        ],

        "conclusion":

            "Conclude with balanced policy recommendations."
    }


# =========================================================
# MASTER EDITORIAL
# =========================================================

def generate_editorial(

    title,
    category

):

    return {

        "gs_paper":

            detect_gs_paper(
                category
            ),

        "background":

            generate_background(
                title,
                category
            ),

        "significance":

            generate_significance(
                title,
                category
            ),

        "mains_question":

            generate_mains_question(
                title,
                category
            ),

        "answer_framework":

            generate_answer_framework(
                title,
                category
            )
    }


# =========================================================
# UI SAFE VERSION
# =========================================================

def generate_editorial_ui(

    title,
    category

):

    editorial = generate_editorial(

        title,
        category
    )

    return {

        "gs_paper":

            editorial[
                "gs_paper"
            ],

        "background":

            editorial[
                "background"
            ],

        "significance":

            " | ".join(
                editorial[
                    "significance"
                ]
            ),

        "mains_question":

            editorial[
                "mains_question"
            ],

        "answer_framework":

            editorial[
                "answer_framework"
            ]
    }