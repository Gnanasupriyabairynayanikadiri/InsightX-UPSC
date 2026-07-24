# =========================================================
# 📁 FILE: core/generators/mains.py
# UPSC MAINS ANSWER GENERATOR ENGINE
# FINAL MODULAR VERSION
# =========================================================


# =========================================================
# DOMAIN KNOWLEDGE MAP
# =========================================================
DOMAIN_KNOWLEDGE = {

    "economy": [

        "inflation",
        "gdp",
        "fiscal deficit",
        "rbi",
        "budget",
        "trade",
        "investment",
        "employment"
    ],

    "geography": [

        "strait",
        "river",
        "ocean",
        "climate",
        "monsoon",
        "mountain",
        "border"
    ],

    "polity": [

        "constitution",
        "supreme court",
        "parliament",
        "governance",
        "federalism",
        "judiciary"
    ],

    "international_relations": [

        "china",
        "usa",
        "quad",
        "g20",
        "un",
        "war",
        "diplomacy"
    ],

    "environment": [

        "climate change",
        "carbon",
        "biodiversity",
        "green energy",
        "pollution"
    ],

    "science_technology": [

        "ai",
        "artificial intelligence",
        "satellite",
        "isro",
        "semiconductor",
        "cyber security"
    ]
}


# =========================================================
# DOMAIN DETECTOR
# =========================================================
def detect_domain(title, category):

    text = f"""
    {title}
    {category}
    """.lower()

    for domain, keywords in DOMAIN_KNOWLEDGE.items():

        for keyword in keywords:

            if keyword in text:

                return domain

    return "general"


# =========================================================
# INTRO GENERATOR
# =========================================================
def generate_intro(

    title,

    category,

    domain,

    region="Global"
):

    return f"""
The issue of "{title}" is an important development under {category}.

It reflects evolving trends in {domain.replace('_', ' ')},
with implications for governance, economy, strategic stability,
and India's broader policy framework in the {region} context.
""".strip()


# =========================================================
# BODY GENERATOR
# =========================================================
def generate_body(domain, region="Global"):

    body = [

        "1. Governance / Policy Dimension",

        "- Institutional response and policy framework",
        "- Administrative efficiency and implementation challenges",

        "",

        "2. Economic Dimension",

        "- Impact on growth, employment, and investment",
        "- Fiscal and trade implications",

        "",

        "3. Geopolitical / Strategic Dimension",

        f"- Strategic relevance in {region}",
        "- India's global positioning and diplomacy",

        "",

        "4. Social / Environmental Dimension",

        "- Impact on citizens and sustainable development",
        "- Climate and social justice concerns",

        "",

        "5. Security Dimension",

        "- National security implications",
        "- Internal and external strategic concerns"
    ]

    # =====================================================
    # DOMAIN ADDONS
    # =====================================================
    domain_addons = {

        "economy":
            "- Financial stability and macroeconomic resilience are critical.",

        "geography":
            "- Geographical location significantly shapes strategic importance.",

        "polity":
            "- Constitutional accountability and institutional balance are essential.",

        "international_relations":
            "- Strategic autonomy and multilateral engagement are necessary.",

        "environment":
            "- Climate sustainability and ecological balance are key priorities.",

        "science_technology":
            "- Technological self-reliance and innovation capacity are vital.",

        "general":
            "- Integrated policy coordination is required."
    }

    body.append("")
    body.append("6. Domain-Specific Insight")
    body.append(domain_addons.get(domain))

    return "\n".join(body)


# =========================================================
# CONCLUSION GENERATOR
# =========================================================
def generate_conclusion(domain):

    conclusions = {

        "economy":
            "India must focus on resilient and inclusive economic reforms for long-term growth.",

        "geography":
            "Balanced regional development and geographical awareness are essential for strategic planning.",

        "polity":
            "Strengthening democratic institutions and governance mechanisms remains crucial.",

        "international_relations":
            "India should continue pursuing strategic autonomy with active global engagement.",

        "environment":
            "Sustainable development and climate responsibility must remain policy priorities.",

        "science_technology":
            "Innovation and technological self-reliance are central to India's future growth.",

        "general":
            "A balanced and forward-looking policy approach is required to address emerging challenges."
    }

    return conclusions.get(
        domain,
        conclusions["general"]
    )


# =========================================================
# PYQ INTELLIGENCE
# =========================================================
def generate_pyq_intelligence(

    category,

    domain
):

    return {

        "GS_relevance": category,

        "repeated_themes": [

            f"{domain} related questions frequently appear in UPSC Mains.",

            "Governance and implementation challenges",

            "India's strategic and developmental priorities",

            "Sustainable development and resilience",

            "Institutional reforms and accountability"
        ],

        "answer_utility":
            "High probability Mains theme",

        "mains_hint":
            "Use multidimensional analysis with examples."
    }


# =========================================================
# MAINS QUESTION GENERATOR
# =========================================================
def generate_mains_question(

    title,

    category
):

    templates = {

        "Polity":
            f"Discuss the constitutional and governance implications of '{title}'.",

        "Economy":
            f"Examine the economic significance of '{title}' for India.",

        "International Relations":
            f"Analyze the geopolitical implications of '{title}' for India.",

        "Environment":
            f"Discuss the environmental and sustainability dimensions of '{title}'.",

        "Science & Technology":
            f"Evaluate the significance of '{title}' in India's technological development.",

        "Social Issues":
            f"Discuss the social and developmental implications of '{title}'."
    }

    return templates.get(

        category,

        f"Discuss the significance of '{title}' for India."
    )


# =========================================================
# MAIN UPSC ANSWER ENGINE
# =========================================================
def generate_upsc_model_answer(

    title,

    category,

    geo=None,

    depth="medium"
):

    # =====================================================
    # REGION
    # =====================================================
    region = "Global"

    if geo:

        region = geo.get(
            "region",
            "Global"
        )

    # =====================================================
    # DOMAIN DETECTION
    # =====================================================
    domain = detect_domain(
        title,
        category
    )

    # =====================================================
    # INTRO
    # =====================================================
    intro = generate_intro(

        title,

        category,

        domain,

        region
    )

    # =====================================================
    # BODY
    # =====================================================
    body = generate_body(

        domain,

        region
    )

    # =====================================================
    # CONCLUSION
    # =====================================================
    conclusion = generate_conclusion(
        domain
    )

    # =====================================================
    # PYQ ENGINE
    # =====================================================
    pyq = generate_pyq_intelligence(

        category,

        domain
    )

    # =====================================================
    # FINAL STRUCTURE
    # =====================================================
    return {

        "intro": intro,

        "body": body,

        "conclusion": conclusion,

        "domain_detected": domain,

        "pyq_intelligence": pyq
    }