# =========================================================
# FILE: app/services/editorial_engine.py
# UPSC EDITORIAL ANALYSIS ENGINE
# =========================================================

import re

print("EDITORIAL_ENGINE LOADED")

# =========================================================
# GS PAPER MAPPING
# =========================================================

CATEGORY_TO_GS = {

    "Polity": "GS Paper II",

    "International Relations": "GS Paper II",

    "Social Issues": "GS Paper II",

    "Economy": "GS Paper III",

    "Environment": "GS Paper III",

    "Science & Technology": "GS Paper III",

    "Security": "GS Paper III",

    "History": "GS Paper I",

    "Geography": "GS Paper I",

    "Misc": "General Studies"

}

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# GS PAPER
# =========================================================

def detect_gs_paper(category):

    return CATEGORY_TO_GS.get(

        category,

        "General Studies"

    )


# =========================================================
# EDITORIAL SUMMARY
# =========================================================

def generate_editorial_summary(title, category):

    title = clean_text(title)

    templates = {

        "Polity":
            f"{title} is significant as it concerns constitutional governance, institutions, democratic accountability and public policy.",

        "Economy":
            f"{title} has important implications for India's economy, fiscal policy, investment climate and economic reforms.",

        "Environment":
            f"{title} is relevant in the context of climate change, biodiversity conservation and sustainable development.",

        "International Relations":
            f"{title} is important from the perspective of India's foreign policy, diplomacy, strategic partnerships and geopolitical interests.",

        "Science & Technology":
            f"{title} highlights recent developments in science, technology, innovation and their governance implications.",

        "Security":
            f"{title} is significant for India's internal security, defence preparedness and strategic interests.",

        "History":
            f"{title} provides historical relevance useful for understanding India's cultural and political evolution.",

        "Geography":
            f"{title} is important from geographical, environmental and resource management perspectives.",

        "Social Issues":
            f"{title} is relevant for understanding welfare, education, health and inclusive development.",

        "Misc":
            f"{title} has relevance for governance and contemporary public policy."

    }

    return templates.get(category, templates["Misc"])


# =========================================================
# BACKGROUND
# =========================================================

def generate_background(title, category):

    title = clean_text(title)

    templates = {

        "Polity":

            (
                f"The development regarding '{title}' should be understood in the broader context "
                "of the Constitution, democratic institutions, governance reforms, federalism "
                "and judicial accountability."
            ),

        "Economy":

            (
                f"The issue '{title}' is connected with India's macroeconomic stability, "
                "economic reforms, fiscal policy, investment climate, employment generation "
                "and sustainable economic growth."
            ),

        "Environment":

            (
                f"The issue '{title}' relates to biodiversity conservation, climate commitments, "
                "renewable energy, pollution control and India's sustainable development goals."
            ),

        "International Relations":

            (
                f"The development '{title}' should be analysed from the perspective of India's "
                "foreign policy, strategic autonomy, bilateral relations, multilateral diplomacy "
                "and regional security."
            ),

        "Science & Technology":

            (
                f"The issue '{title}' highlights advances in technology, innovation, digital governance, "
                "research, emerging technologies and their socio-economic implications."
            ),

        "Security":

            (
                f"The issue '{title}' concerns India's internal security architecture, defence preparedness, "
                "counter-terrorism strategy, border management and strategic capabilities."
            ),

        "History":

            (
                f"The topic '{title}' is important for understanding India's historical evolution, "
                "cultural heritage and socio-political developments."
            ),

        "Geography":

            (
                f"The issue '{title}' is relevant from the perspective of physical geography, "
                "resource distribution, environmental management and regional planning."
            ),

        "Social Issues":

            (
                f"The issue '{title}' is associated with social justice, welfare programmes, "
                "education, healthcare, gender issues and inclusive development."
            ),

        "Misc":

            (
                f"The issue '{title}' has important governance and policy implications "
                "for contemporary India."
            )

    }

    return templates.get(category, templates["Misc"])

# =========================================================
# SIGNIFICANCE
# =========================================================

def generate_significance(category):

    mapping = {

        "Polity":[

            "Constitutional governance",

            "Institutional accountability",

            "Federal structure",

            "Democratic reforms"

        ],

        "Economy":[

            "Macroeconomic stability",

            "Inclusive growth",

            "Fiscal reforms",

            "Employment generation"

        ],

        "Environment":[

            "Climate resilience",

            "Biodiversity conservation",

            "Renewable energy",

            "Sustainable development"

        ],

        "International Relations":[

            "India's foreign policy",

            "Strategic partnerships",

            "Regional security",

            "Global diplomacy"

        ],

        "Science & Technology":[

            "Innovation ecosystem",

            "Digital governance",

            "Research & Development",

            "Emerging technologies"

        ],

        "Security":[

            "Internal security",

            "Border management",

            "Counter-terrorism",

            "Strategic preparedness"

        ],

        "History":[

            "Historical relevance",

            "Cultural heritage",

            "Freedom movement",

            "Nation building"

        ],

        "Geography":[

            "Resource management",

            "Disaster resilience",

            "Regional planning",

            "Environmental sustainability"

        ],

        "Social Issues":[

            "Inclusive development",

            "Social justice",

            "Education",

            "Public health"

        ]

    }

    return mapping.get(

        category,

        [

            "Governance",

            "Policy relevance",

            "Current affairs"

        ]

    )


# =========================================================
# PRELIMS FOCUS
# =========================================================

def generate_prelims_focus(title, category):

    mapping = {

        "Polity":[

            "Constitutional Articles",

            "Important Bills & Acts",

            "Constitutional Bodies",

            "Supreme Court Judgments"

        ],

        "Economy":[

            "RBI",

            "Budget",

            "Economic Survey",

            "Important Reports"

        ],

        "Environment":[

            "National Parks",

            "Species in News",

            "Climate Agreements",

            "Environmental Conventions"

        ],

        "International Relations":[

            "Countries in News",

            "International Organisations",

            "Summits",

            "Strategic Groupings"

        ],

        "Science & Technology":[

            "Emerging Technologies",

            "ISRO Missions",

            "AI",

            "Government Technology Initiatives"

        ],

        "Security":[

            "Security Agencies",

            "Military Exercises",

            "Border Areas",

            "Internal Security"

        ],

        "History":[

            "Important Personalities",

            "Timeline",

            "Architecture",

            "Culture"

        ],

        "Geography":[

            "Maps",

            "Locations",

            "Resources",

            "Climate"

        ],

        "Social Issues":[

            "Government Schemes",

            "Reports",

            "Indices",

            "Committees"

        ]

    }

    return mapping.get(

        category,

        [

            "Current Affairs",

            "Government Reports",

            "Important Facts",

            "Static Linkages"

        ]

    )


# =========================================================
# MAINS FOCUS
# =========================================================

def generate_mains_focus(category):

    mapping = {

        "Polity":

            "Constitutional reforms, governance, accountability, transparency and institutional effectiveness.",

        "Economy":

            "Economic reforms, inflation, fiscal management, inclusive growth and employment.",

        "Environment":

            "Climate action, conservation, sustainable development and environmental governance.",

        "International Relations":

            "India's foreign policy, diplomacy, regional security and strategic partnerships.",

        "Science & Technology":

            "Innovation, regulation, emerging technologies and socio-economic impact.",

        "Security":

            "National security, defence preparedness, terrorism and cyber security.",

        "History":

            "Historical evolution and relevance in contemporary governance.",

        "Geography":

            "Resource utilisation, environmental management and regional planning.",

        "Social Issues":

            "Social justice, education, healthcare and inclusive development."

    }

    return mapping.get(

        category,

        "Governance and policy implications."

    )


# =========================================================
# MAINS QUESTION
# =========================================================

def generate_mains_question(title, category):

    title = clean_text(title)

    templates = {

        "Polity":

            f"Discuss the constitutional, governance and institutional implications of '{title}'.",

        "Economy":

            f"Analyse the economic implications of '{title}' and suggest suitable policy measures.",

        "Environment":

            f"Discuss the environmental significance of '{title}' in the context of sustainable development.",

        "International Relations":

            f"Evaluate the impact of '{title}' on India's foreign policy and strategic interests.",

        "Science & Technology":

            f"Discuss the role of science and technology in the context of '{title}' and its governance implications.",

        "Security":

            f"Assess the security implications of '{title}' for India.",

        "History":

            f"Discuss the historical significance of '{title}' and its relevance today.",

        "Geography":

            f"Examine the geographical dimensions associated with '{title}'.",

        "Social Issues":

            f"Discuss the social and governance challenges associated with '{title}'."

    }

    return templates.get(

        category,

        f"Discuss the significance of '{title}' from the UPSC perspective."

    )

# =========================================================
# ANSWER FRAMEWORK
# =========================================================

def generate_answer_framework():

    return {

        "Introduction":
            "Briefly introduce the issue with current context.",

        "Body": [

            "Background",

            "Current Developments",

            "Importance",

            "Challenges",

            "Government Initiatives",

            "Way Forward"

        ],

        "Conclusion":
            "Provide a balanced conclusion with reforms and future outlook."

    }


# =========================================================
# STRUCTURED EDITORIAL
# =========================================================

def generate_editorial_structured(title, category):

    return {

        "gs_paper":

            detect_gs_paper(category),

        "background":

            generate_background(title, category),

        "significance":

            generate_significance(category),

        "prelims_focus":

            generate_prelims_focus(title, category),

        "mains_focus":

            generate_mains_focus(category),

        "mains_question":

            generate_mains_question(title, category),

        "answer_framework":

            generate_answer_framework()

    }


# =========================================================
# COMPLETE EDITORIAL (DATABASE SAFE)
# =========================================================

def generate_editorial(title, category):

    title = clean_text(title)

    gs = detect_gs_paper(category)

    summary = generate_editorial_summary(title, category)

    background = generate_background(title, category)

    mains_focus = generate_mains_focus(category)

    prelims = ", ".join(

        generate_prelims_focus(title, category)

    )

    return (

        f"{gs}\n\n"

        f"Summary:\n"

        f"{summary}\n\n"

        f"Background:\n"

        f"{background}\n\n"

        f"Prelims Focus:\n"

        f"{prelims}\n\n"

        f"Mains Focus:\n"

        f"{mains_focus}"

    )


# =========================================================
# UPSC INSIGHT
# =========================================================

def generate_upsc_insight(title, category):

    title = clean_text(title)

    insights = {

        "Polity":

            (
                f"'{title}' is important for understanding constitutional provisions, "
                "governance reforms, judicial developments and democratic institutions."
            ),

        "Economy":

            (
                f"'{title}' should be linked with economic reforms, "
                "RBI policies, Budget, inflation, growth and employment."
            ),

        "Environment":

            (
                f"'{title}' is relevant for climate change, biodiversity, "
                "international conventions and sustainable development."
            ),

        "International Relations":

            (
                f"'{title}' is useful for understanding India's bilateral relations, "
                "global diplomacy, strategic partnerships and geopolitical developments."
            ),

        "Science & Technology":

            (
                f"'{title}' highlights technological innovation, "
                "digital governance, emerging technologies and scientific research."
            ),

        "Security":

            (
                f"'{title}' is important from the perspective of "
                "national security, defence preparedness and strategic affairs."
            ),

        "History":

            (
                f"'{title}' provides historical context useful for "
                "UPSC GS Paper I and culture-related questions."
            ),

        "Geography":

            (
                f"'{title}' is useful for understanding geographical processes, "
                "resource management and environmental planning."
            ),

        "Social Issues":

            (
                f"'{title}' should be linked with welfare schemes, "
                "social justice, education and healthcare."
            )

    }

    return insights.get(

        category,

        f"'{title}' has governance and policy relevance."

    )


