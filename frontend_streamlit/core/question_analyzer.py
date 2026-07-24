# =========================================================
# 📁 FILE: core/question_analyzer.py
# =========================================================

import re


# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()


# =========================================================
# EXTRACT KEYWORDS
# =========================================================
def extract_keywords(question):

    stop_words = [

        "the",
        "is",
        "are",
        "was",
        "were",
        "a",
        "an",
        "of",
        "in",
        "on",
        "with",
        "and",
        "or",
        "to",
        "for",
        "from",
        "by",
        "what",
        "why",
        "how"
    ]

    question = clean_text(question)

    words = question.split()

    keywords = []

    for word in words:

        if word not in stop_words and len(word) > 2:

            keywords.append(word)

    return list(set(keywords))


# =========================================================
# DETECT DIRECTIVE
# =========================================================
def detect_directive(question):

    question = question.lower()

    directives = {

        "discuss": "Discussion",

        "explain": "Explanation",

        "examine": "Examination",

        "analyze": "Analysis",

        "evaluate": "Evaluation",

        "critically examine": "Critical Examination",

        "critically analyze": "Critical Analysis",

        "comment": "Commentary",

        "elucidate": "Elaboration",

        "differentiate": "Comparison",

        "distinguish": "Distinction",

        "write a short note": "Short Note",

        "trace": "Historical Trace",

        "highlight": "Highlighting",

        "describe": "Description"
    }

    for key in directives:

        if key in question:

            return directives[key]

    return "General Discussion"


# =========================================================
# DETECT QUESTION TYPE
# =========================================================
def detect_question_type(question):

    question = question.lower()

    # =====================================================
    # STATIC SUBJECTS
    # =====================================================
    static_keywords = [

        "history",
        "architecture",
        "temple",
        "culture",
        "harappan",
        "mauryan",
        "gupta",
        "chola",
        "pallava",
        "khajuraho",
        "odisha",
        "buddhism",
        "jainism",
        "art"
    ]

    # =====================================================
    # CURRENT AFFAIRS
    # =====================================================
    current_keywords = [

        "scheme",
        "budget",
        "government",
        "policy",
        "india",
        "economy",
        "climate",
        "technology",
        "international",
        "security"
    ]

    for word in static_keywords:

        if word in question:

            return "Static"

    for word in current_keywords:

        if word in question:

            return "Current Affairs"

    return "General"


# =========================================================
# DETECT DIFFICULTY
# =========================================================
def detect_difficulty(question):

    question = question.lower()

    # =====================================================
    # ADVANCED
    # =====================================================
    advanced_words = [

        "critically",
        "analyze",
        "evaluate",
        "comment",
        "justify",
        "assess"
    ]

    # =====================================================
    # MODERATE
    # =====================================================
    moderate_words = [

        "examine",
        "discuss",
        "differentiate",
        "distinguish",
        "compare"
    ]

    for word in advanced_words:

        if word in question:

            return "Advanced"

    for word in moderate_words:

        if word in question:

            return "Moderate"

    return "Basic"


# =========================================================
# EXPECTED STRUCTURE
# =========================================================
def expected_structure(question):

    directive = detect_directive(question)

    structure = [

        "Introduction",

        "Body",

        "Conclusion"
    ]

    # =====================================================
    # ANALYTICAL QUESTIONS
    # =====================================================
    if directive in [

        "Analysis",
        "Evaluation",
        "Critical Analysis",
        "Critical Examination"
    ]:

        structure = [

            "Introduction",

            "Core Analysis",

            "Challenges / Limitations",

            "Way Forward",

            "Conclusion"
        ]

    # =====================================================
    # COMPARISON QUESTIONS
    # =====================================================
    elif directive in [

        "Comparison",
        "Distinction"
    ]:

        structure = [

            "Introduction",

            "Comparison Table / Differences",

            "Examples",

            "Conclusion"
        ]

    # =====================================================
    # SHORT NOTE
    # =====================================================
    elif directive == "Short Note":

        structure = [

            "Introduction",

            "Key Features",

            "Significance",

            "Conclusion"
        ]

    return structure


# =========================================================
# SUBJECT DETECTION
# =========================================================
def detect_subject(question):

    question = question.lower()

    subjects = {

        "history": "History",

        "architecture": "Art & Culture",

        "economy": "Economy",

        "polity": "Polity",

        "environment": "Environment",

        "science": "Science & Technology",

        "society": "Society",

        "ethics": "Ethics",

        "security": "Internal Security",

        "international": "International Relations"
    }

    for key in subjects:

        if key in question:

            return subjects[key]

    return "General Studies"


# =========================================================
# UPSC INSIGHTS
# =========================================================
def generate_upsc_insights(question):

    directive = detect_directive(question)

    difficulty = detect_difficulty(question)

    question_type = detect_question_type(question)

    insights = {

        "Question Type": question_type,

        "Difficulty Level": difficulty,

        "Directive Meaning": directive,

        "Subject Area": detect_subject(question)
    }

    return insights


# =========================================================
# MAIN ANALYZER FUNCTION
# =========================================================
def analyze_question(question):

    analysis = {

        "type": detect_question_type(question),

        "directive": detect_directive(question),

        "difficulty": detect_difficulty(question),

        "keywords": extract_keywords(question),

        "structure": expected_structure(question),

        "subject": detect_subject(question),

        "insights": generate_upsc_insights(question)
    }

    return analysis