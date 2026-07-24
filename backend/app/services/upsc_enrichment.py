# =========================================================
# FILE: app/services/upsc_enrichment.py
# UPSC ENRICHMENT ENGINE
# =========================================================

import re

print("UPSC_ENRICHMENT LOADED")


# =========================================================
# PRELIMS FOCUS
# =========================================================

def generate_prelims_focus(title: str, category: str):

    category = str(category).lower()

    mapping = {

        "economy": [

            "Budget",
            "Economic Survey",
            "GDP",
            "Inflation",
            "RBI",
            "SEBI",
            "Fiscal Policy",
            "Monetary Policy"

        ],

        "polity": [

            "Constitution",
            "Articles",
            "Supreme Court",
            "Parliament",
            "Bills",
            "Acts",
            "Constitutional Bodies",
            "Governance"

        ],

        "environment": [

            "Climate Change",
            "UNFCCC",
            "COP Summits",
            "Ramsar Sites",
            "Biodiversity",
            "National Parks",
            "Species in News",
            "Environmental Conventions"

        ],

        "science": [

            "Artificial Intelligence",
            "Semiconductors",
            "Quantum Technology",
            "ISRO",
            "Space Missions",
            "Biotechnology",
            "Cyber Security",
            "Emerging Technologies"

        ],

        "international": [

            "India's Foreign Policy",
            "UN",
            "BRICS",
            "G20",
            "QUAD",
            "ASEAN",
            "Strategic Partnerships",
            "Global Organisations"

        ],

        "security": [

            "Internal Security",
            "Border Security",
            "Counter Terrorism",
            "Cyber Security",
            "Defence Exercises",
            "Military Technology"

        ]

    }

    for key in mapping:

        if key in category:

            return mapping[key]

    return [

        "Current Affairs",
        "Government Schemes",
        "Important Reports",
        "Static Linkages"

    ]


# =========================================================
# MAINS QUESTION
# =========================================================

def generate_mains_question(title: str, category: str):

    title = str(title)

    category = category.lower()

    if "economy" in category:

        return f"Discuss the economic implications of '{title}' and suggest suitable policy measures."

    if "polity" in category:

        return f"Discuss the constitutional and governance implications of '{title}'."

    if "environment" in category:

        return f"Examine the environmental significance of '{title}' in the context of sustainable development."

    if "international" in category:

        return f"Evaluate the impact of '{title}' on India's foreign policy and strategic interests."

    if "science" in category:

        return f"Discuss the role of science and technology in '{title}' and its implications for India."

    if "security" in category:

        return f"Assess the security implications of '{title}' for India."

    return f"Discuss the significance of '{title}' from a UPSC perspective."


# =========================================================
# BACKGROUND
# =========================================================

def generate_background(title: str, category: str):

    title = str(title)

    category = category.lower()

    if "economy" in category:

        return f"'{title}' is associated with India's macroeconomic stability, fiscal reforms and inclusive growth."

    if "polity" in category:

        return f"'{title}' relates to constitutional governance, democratic institutions and public administration."

    if "environment" in category:

        return f"'{title}' is linked to biodiversity conservation, climate commitments and environmental governance."

    if "international" in category:

        return f"'{title}' has implications for India's diplomacy, strategic partnerships and geopolitical interests."

    if "science" in category:

        return f"'{title}' highlights innovation, technological advancement and India's scientific capabilities."

    if "security" in category:

        return f"'{title}' concerns national security, defence preparedness and strategic affairs."

    return f"'{title}' has governance and policy relevance."


# =========================================================
# TAG GENERATOR
# =========================================================

def generate_tags(title: str, category: str):

    text = f"{title} {category}".lower()

    tags = []

    TAG_MAP = {

        "constitution": "Constitution",
        "parliament": "Parliament",
        "judiciary": "Judiciary",
        "supreme court": "Supreme Court",
        "rbi": "RBI",
        "inflation": "Inflation",
        "budget": "Budget",
        "gdp": "GDP",
        "climate": "Climate Change",
        "biodiversity": "Biodiversity",
        "renewable": "Renewable Energy",
        "g20": "G20",
        "brics": "BRICS",
        "quad": "QUAD",
        "asean": "ASEAN",
        "un": "United Nations",
        "isro": "ISRO",
        "artificial intelligence": "AI",
        "ai": "AI",
        "quantum": "Quantum Technology",
        "semiconductor": "Semiconductors"

    }

    for key, value in TAG_MAP.items():

        if key in text:

            tags.append(value)

    if category:

        tags.insert(0, category)

    tags = list(dict.fromkeys(tags))

    return tags if tags else ["Current Affairs"]


# =========================================================
# MCQ GENERATOR
# =========================================================

def generate_mcqs(title: str, category: str):

    return [

        {

            "question": f"{title} is primarily associated with which UPSC theme?",

            "options": [

                category,

                "Economy",

                "Environment",

                "Polity"

            ],

            "answer": category

        }

    ]


# =========================================================
# COMPLETE WRAPPER
# =========================================================

def generate_enrichment(title: str, category: str):

    return {

        "background": generate_background(title, category),

        "prelims_focus": generate_prelims_focus(title, category),

        "mains_question": generate_mains_question(title, category),

        "tags": generate_tags(title, category),

        "mcqs": generate_mcqs(title, category)

    }