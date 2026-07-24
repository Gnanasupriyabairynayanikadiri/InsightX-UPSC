# =========================================================
# FILE: core/current_affairs/upsc_enrichment.py
# FINAL UPSC ENRICHMENT ENGINE
# =========================================================


# =========================================================
# CATEGORY PRELIMS FOCUS
# =========================================================

PRELIMS_FOCUS = {

    "Polity": [
        "Constitutional provisions",
        "Important Articles",
        "Supreme Court judgments",
        "Parliamentary procedures",
        "Governance reforms"
    ],

    "Economy": [
        "Inflation",
        "GDP trends",
        "RBI policies",
        "Fiscal policy",
        "Economic indicators"
    ],

    "Environment": [
        "Climate Change",
        "Biodiversity",
        "Environmental conventions",
        "Conservation initiatives",
        "Pollution control"
    ],

    "Science & Technology": [
        "Emerging technologies",
        "Artificial Intelligence",
        "ISRO missions",
        "Semiconductors",
        "Cyber security"
    ],

    "International Relations": [
        "India's Foreign Policy",
        "Global Organizations",
        "Strategic Partnerships",
        "Geopolitical Developments",
        "Multilateral Forums"
    ],

    "Social Issues": [
        "Education",
        "Healthcare",
        "Nutrition",
        "Women Empowerment",
        "Social Welfare"
    ]
}


# =========================================================
# CATEGORY BACKGROUND
# =========================================================

BACKGROUND_TEMPLATES = {

    "Polity":
        "The issue is important for governance, constitutional institutions and public administration.",

    "Economy":
        "The issue is relevant for understanding India's economic growth, fiscal policy and financial stability.",

    "Environment":
        "The issue is linked to climate change, sustainability and ecological conservation.",

    "Science & Technology":
        "The development reflects advances in innovation, research and technology policy.",

    "International Relations":
        "The issue has implications for India's foreign policy and strategic interests.",

    "Social Issues":
        "The issue impacts social development, welfare and inclusive growth."
}


# =========================================================
# CATEGORY MAINS TEMPLATES
# =========================================================

MAINS_TEMPLATES = {

    "Polity":
        "Discuss the constitutional and governance implications of {title}.",

    "Economy":
        "Analyze the economic significance of {title}.",

    "Environment":
        "Examine the environmental implications of {title}.",

    "Science & Technology":
        "Discuss the role of science and technology in relation to {title}.",

    "International Relations":
        "Evaluate the impact of {title} on India's foreign policy.",

    "Social Issues":
        "Discuss the social significance of {title}."
}


# =========================================================
# UPSC TAG DATABASE
# =========================================================

TAG_KEYWORDS = {

    # POLITY
    "constitution": "Constitution",
    "supreme court": "Supreme Court",
    "parliament": "Parliament",
    "judiciary": "Judiciary",
    "election": "Election",

    # ECONOMY
    "inflation": "Inflation",
    "rbi": "RBI",
    "gdp": "GDP",
    "budget": "Budget",
    "economy": "Economy",
    "tax": "Taxation",

    # ENVIRONMENT
    "climate": "Climate Change",
    "biodiversity": "Biodiversity",
    "forest": "Forests",
    "cop": "COP Summit",
    "pollution": "Pollution",

    # SCIENCE
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "isro": "ISRO",
    "quantum": "Quantum Technology",
    "semiconductor": "Semiconductor",

    # IR
    "g20": "G20",
    "brics": "BRICS",
    "china": "China",
    "usa": "USA",
    "indo-pacific": "Indo-Pacific",

    # SECURITY
    "terror": "Internal Security",
    "cyber": "Cyber Security",
    "defence": "Defence"
}


# =========================================================
# PRELIMS FOCUS
# =========================================================

def generate_prelims_focus(title, category):

    return PRELIMS_FOCUS.get(
        category,
        [
            "Current Affairs",
            "Government Policies",
            "UPSC Relevance"
        ]
    )


# =========================================================
# MAINS QUESTION
# =========================================================

def generate_mains_question(title, category):

    template = MAINS_TEMPLATES.get(
        category,
        "Discuss the significance of {title}."
    )

    return template.format(title=title)


# =========================================================
# BACKGROUND
# =========================================================

def generate_background(title, category):

    return BACKGROUND_TEMPLATES.get(
        category,
        "Relevant for UPSC preparation."
    )


# =========================================================
# UPSC TAGS
# =========================================================

def generate_tags(title, category="General Studies"):

    text = f"{title} {category}".lower()

    tags = []

    for keyword, tag in TAG_KEYWORDS.items():

        if keyword in text:

            if tag not in tags:
                tags.append(tag)

    if category not in tags:
        tags.insert(0, category)

    if not tags:
        tags = ["Current Affairs"]

    return tags


# =========================================================
# MCQ GENERATOR
# =========================================================

def generate_mcqs(title, category):

    options = [

        "Polity",
        "Economy",
        "Environment",
        "Science & Technology"
    ]

    if category not in options:
        options[-1] = category

    return [

        {
            "question":
                f"{title} is primarily related to which area?",

            "options":
                options,

            "answer":
                category
        }
    ]


# =========================================================
# QUICK REVISION NOTES
# =========================================================

def generate_revision_points(title, category):

    return [

        f"Understand the background of {title}.",

        f"Revise static syllabus linked with {category}.",

        f"Prepare UPSC Prelims facts related to {title}.",

        f"Prepare Mains dimensions of {title}.",

        "Revise government initiatives and reports."
    ]


# =========================================================
# UPSC TAKEAWAY
# =========================================================

def generate_upsc_takeaway(title, category):

    return (
        f"{title} is important from "
        f"{category} perspective and should be linked "
        f"with static syllabus for UPSC preparation."
    )