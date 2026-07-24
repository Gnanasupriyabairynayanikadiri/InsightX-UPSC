# =========================================================
# 📁 FILE: core/evaluator.py
# =========================================================

import re


# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# EXTRACT KEYWORDS
# =========================================================
def extract_keywords(question):

    question = clean_text(question)

    stopwords = {

        "the",
        "is",
        "are",
        "was",
        "were",
        "what",
        "why",
        "how",
        "when",
        "where",
        "which",
        "discuss",
        "examine",
        "evaluate",
        "analyse",
        "analyze",
        "write",
        "short",
        "note",
        "features",
        "main",
        "with",
        "suitable",
        "examples",
        "of",
        "on",
        "in",
        "and",
        "to",
        "for",
        "a",
        "an",
        "the"
    }

    words = question.split()

    keywords = []

    for word in words:

        if len(word) > 3 and word not in stopwords:

            keywords.append(word)

    return list(set(keywords))


# =========================================================
# STRICT TOPIC MATCH DETECTOR
# =========================================================
def detect_topic_match(question, answer):

    question_clean = clean_text(question)

    answer_clean = clean_text(answer)

    # =====================================================
    # IMPORTANT QUESTION KEYWORDS
    # =====================================================
    important_keywords = extract_keywords(question)

    matched_keywords = []

    matched = 0

    for keyword in important_keywords:

        if keyword in answer_clean:

            matched += 1

            matched_keywords.append(keyword)

    # =====================================================
    # MATCH %
    # =====================================================
    if len(important_keywords) == 0:

        return True, 100, matched_keywords

    match_percentage = (

        matched / len(important_keywords)
    ) * 100

    # =====================================================
    # WRONG TOPIC WORDS
    # =====================================================
    wrong_topic_words = [

        # DYNASTIES
        "gupta",
        "maurya",
        "harappan",
        "mughal",
        "pallava",
        "chola",

        # WRONG ARCHITECTURE
        "nagara",

        # WRONG SITES
        "deogarh",
        "bhitargaon",

        # WRONG CIVILIZATION
        "indus",

        # OTHER TOPICS
        "ashoka",
        "buddhist",
        "sanchi"
    ]

    # =====================================================
    # VIJAYANAGARA STRICT CHECK
    # =====================================================
    if "vijayanagara" in question_clean:

        required_words = [

            "vijayanagara",
            "hampi",
            "gopuram",
            "mandapa",
            "dravidian",
            "virupaksha",
            "vittala"
        ]

        required_match = 0

        for word in required_words:

            if word in answer_clean:

                required_match += 1

        # =================================================
        # FAIL IF CORE TERMS ABSENT
        # =================================================
        if required_match < 2:

            return False, match_percentage, matched_keywords

    # =====================================================
    # ODISHA STRICT CHECK
    # =====================================================
    if "odisha" in question_clean:

        required_words = [

            "rekha",
            "deula",
            "jagamohana",
            "konark",
            "lingaraja",
            "kalinga"
        ]

        required_match = 0

        for word in required_words:

            if word in answer_clean:

                required_match += 1

        if required_match < 2:

            return False, match_percentage, matched_keywords

    # =====================================================
    # KHJURAHO STRICT CHECK
    # =====================================================
    if "khajuraho" in question_clean:

        required_words = [

            "khajuraho",
            "chandela",
            "shikhara",
            "sandstone",
            "sculpture",
            "nagara"
        ]

        required_match = 0

        for word in required_words:

            if word in answer_clean:

                required_match += 1

        if required_match < 2:

            return False, match_percentage, matched_keywords

    # =====================================================
    # HARAPPAN STRICT CHECK
    # =====================================================
    if "harappan" in question_clean:

        required_words = [

            "drainage",
            "citadel",
            "granary",
            "great bath",
            "town planning",
            "grid"
        ]

        required_match = 0

        for word in required_words:

            if word in answer_clean:

                required_match += 1

        if required_match < 2:

            return False, match_percentage, matched_keywords

    # =====================================================
    # WRONG WORD DETECTION
    # =====================================================
    wrong_matches = 0

    for word in wrong_topic_words:

        if word in answer_clean and word not in question_clean:

            wrong_matches += 1

    # =====================================================
    # FAIL CONDITIONS
    # =====================================================
    if wrong_matches >= 2:

        return False, match_percentage, matched_keywords

    if match_percentage < 40:

        return False, match_percentage, matched_keywords

    return True, match_percentage, matched_keywords


# =========================================================
# STRUCTURE SCORE
# =========================================================
def structure_score(answer):

    score = 0

    answer_lower = answer.lower()

    # INTRODUCTION
    if "introduction" in answer_lower:

        score += 1

    # CONCLUSION
    if "conclusion" in answer_lower:

        score += 1

    # BULLETS / POINTS
    if (

        "1." in answer

        or "•" in answer

        or "-" in answer
    ):

        score += 1

    return score


# =========================================================
# CONTENT SCORE
# =========================================================
def content_score(answer):

    word_count = len(answer.split())

    if word_count >= 350:

        return 4

    elif word_count >= 250:

        return 3

    elif word_count >= 150:

        return 2

    elif word_count >= 80:

        return 1

    return 0


# =========================================================
# EXAMPLE SCORE
# =========================================================
def example_score(answer):

    answer_lower = answer.lower()

    indicators = [

        "example",
        "e.g",
        "for instance",
        "such as",
        "temple",
        "act",
        "scheme"
    ]

    for word in indicators:

        if word in answer_lower:

            return 1

    return 0


# =========================================================
# KEYWORD SCORE
# =========================================================
def keyword_score(question, answer):

    keywords = extract_keywords(question)

    answer_clean = clean_text(answer)

    matched = 0

    for keyword in keywords:

        if keyword in answer_clean:

            matched += 1

    if len(keywords) == 0:

        return 0

    percentage = matched / len(keywords)

    if percentage >= 0.8:

        return 3

    elif percentage >= 0.5:

        return 2

    elif percentage >= 0.3:

        return 1

    return 0


# =========================================================
# MAIN EVALUATION FUNCTION
# =========================================================
def evaluate_answer(question, answer):

    # =====================================================
    # TOPIC MATCH CHECK
    # =====================================================
    topic_match, match_percentage, matched_keywords = (

        detect_topic_match(question, answer)
    )

    # =====================================================
    # WRONG TOPIC
    # =====================================================
    if not topic_match:

        return {

            "score": 1,

            "rank": "⚠️ Needs Improvement",

            "strengths": [],

            "weaknesses": [

                "Answer written on completely different topic",

                "Core demand of question not addressed"
            ],

            "suggestions": [

                "Focus on exact topic asked",

                "Use topic-specific keywords",

                "Read question carefully"
            ],

            "topic_match": False,

            "match_percentage": round(match_percentage, 2),

            "matched_keywords": matched_keywords
        }

    # =====================================================
    # NORMAL EVALUATION
    # =====================================================
    total_score = 0

    strengths = []

    weaknesses = []

    suggestions = []

    # =====================================================
    # STRUCTURE
    # =====================================================
    s_score = structure_score(answer)

    total_score += s_score

    if s_score >= 2:

        strengths.append(

            "Good structure and headings"
        )

    else:

        weaknesses.append(

            "Poor answer structure"
        )

        suggestions.append(

            "Use Introduction, Body and Conclusion"
        )

    # =====================================================
    # CONTENT
    # =====================================================
    c_score = content_score(answer)

    total_score += c_score

    if c_score >= 3:

        strengths.append(

            "Good content depth"
        )

    else:

        weaknesses.append(

            "Insufficient content depth"
        )

        suggestions.append(

            "Add more dimensions and explanations"
        )

    # =====================================================
    # EXAMPLES
    # =====================================================
    e_score = example_score(answer)

    total_score += e_score

    if e_score >= 1:

        strengths.append(

            "Examples used effectively"
        )

    else:

        weaknesses.append(

            "Examples missing"
        )

        suggestions.append(

            "Add relevant examples"
        )

    # =====================================================
    # KEYWORDS
    # =====================================================
    k_score = keyword_score(question, answer)

    total_score += k_score

    if k_score >= 2:

        strengths.append(

            "Good keyword usage"
        )

    else:

        weaknesses.append(

            "Poor keyword coverage"
        )

        suggestions.append(

            "Use more question keywords"
        )

    # =====================================================
    # FINAL SCORE
    # =====================================================
    if total_score > 10:

        total_score = 10

    # =====================================================
    # RANK
    # =====================================================
    if total_score >= 8:

        rank = "🔥 Good Answer"

    elif total_score >= 5:

        rank = "👍 Average Answer"

    else:

        rank = "⚠️ Needs Improvement"

    # =====================================================
    # RESULT
    # =====================================================
    return {

        "score": total_score,

        "rank": rank,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions,

        "topic_match": True,

        "match_percentage": round(match_percentage, 2),

        "matched_keywords": matched_keywords
    }