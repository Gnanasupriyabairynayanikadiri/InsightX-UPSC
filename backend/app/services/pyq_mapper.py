# =========================================================
# 📁 FILE: core/services/pyq_mapper.py
# UPSC PYQ MAPPING ENGINE (FIXED & STABLE)
# =========================================================


# =========================================================
# PYQ DATABASE (STANDARDIZED KEYS)
# =========================================================
PYQ_DATABASE = {
    "economy": [
        "UPSC Prelims 2023: Inflation and Monetary Policy",
        "UPSC Mains GS-3 2022: RBI and Inflation Control"
    ],

    "polity": [
        "UPSC Prelims 2022: Constitutional Amendments",
        "UPSC Mains GS-2 2021: Judicial Review"
    ],

    "environment": [
        "UPSC Prelims 2023: Climate Change",
        "UPSC Mains GS-3 2022: Biodiversity Conservation"
    ],

    "international relations": [
        "UPSC Mains GS-2 2023: India and Global Institutions",
        "UPSC Prelims 2021: International Organizations"
    ],

    "science & technology": [
        "UPSC Prelims 2023: Artificial Intelligence",
        "UPSC Mains GS-3 2022: Emerging Technologies"
    ],

    "social issues": [
        "UPSC Mains GS-1 2022: Education and Social Development"
    ]
}


# =========================================================
# NORMALIZE CATEGORY (CRITICAL FIX)
# =========================================================
def normalize_category(category: str) -> str:

    if not category:
        return "general studies"

    return str(category).strip().lower()


# =========================================================
# MAP PYQ REFERENCES
# =========================================================
def map_pyq_references(title: str, category: str = "General Studies"):

    category_key = normalize_category(category)

    return PYQ_DATABASE.get(category_key, [])


# =========================================================
# SAFE ALIAS (BACKWARD COMPATIBILITY)
# =========================================================
def get_pyq_references(title: str, category: str = "General Studies"):

    return map_pyq_references(title, category)


# =========================================================
# SMART PYQ MATCHING (OPTIONAL UPGRADE LAYER)
# =========================================================
def smart_pyq_match(title: str, category: str):

    title = str(title).lower()
    pyqs = map_pyq_references(title, category)

    matched = []

    for pyq in pyqs:
        if any(word in title for word in pyq.lower().split()):
            matched.append(pyq)

    return matched if matched else pyqs
