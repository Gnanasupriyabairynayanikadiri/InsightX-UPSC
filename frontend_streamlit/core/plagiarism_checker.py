# =========================================================
# 📁 FILE: core/plagiarism_checker.py
# =========================================================

import re
from difflib import SequenceMatcher


# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()


# =========================================================
# SPLIT SENTENCES
# =========================================================
def split_sentences(text):

    sentences = re.split(r"[.!?]", text)

    cleaned = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 15:

            cleaned.append(sentence)

    return cleaned


# =========================================================
# CHECK REPETITION
# =========================================================
def check_repetition(sentences):

    repeated = 0

    for i in range(len(sentences)):

        for j in range(i + 1, len(sentences)):

            similarity = SequenceMatcher(

                None,
                sentences[i],
                sentences[j]

            ).ratio()

            if similarity > 0.90:

                repeated += 1

    return repeated


# =========================================================
# MAIN PLAGIARISM CHECKER
# =========================================================
def check_plagiarism(question, answer):

    # =====================================================
    # CLEAN QUESTION + ANSWER
    # =====================================================
    question_clean = clean_text(question)

    answer_clean = clean_text(answer)

    # =====================================================
    # VERY SHORT ANSWERS
    # =====================================================
    if len(answer_clean.split()) < 30:

        return {

            "similarity": 0,

            "status": "Too Short"
        }

    # =====================================================
    # QUESTION KEYWORDS
    # =====================================================
    question_keywords = question_clean.split()

    answer_keywords = answer_clean.split()

    matched_keywords = 0

    for keyword in question_keywords:

        if keyword in answer_keywords:

            matched_keywords += 1

    keyword_ratio = 0

    if len(question_keywords) > 0:

        keyword_ratio = (

            matched_keywords
            / len(question_keywords)
        )

    # =====================================================
    # AI / COPY PATTERNS
    # =====================================================
    suspicious_patterns = [

        "the topic is important from the upsc examination perspective",

        "define the concept clearly",

        "mention major features",

        "add examples and significance",

        "a balanced and analytical approach",

        "indian architectural traditions reflect",

        "continue to remain important symbols",

        "write concise and structured points",

        "use headings and subheadings",

        "good introduction present",

        "conclusion is present",

        "the harappan civilization represents",

        "odisha temple architecture represents",

        "vijayanagara rulers transformed",

        "khajuraho temples symbolize",

        "dravidian temple architecture",

        "nagara style architecture",

        "the mauryan empire marks",

        "ashoka embraced buddhism",

        "advanced urban planning and engineering"
    ]

    suspicious_matches = 0

    for pattern in suspicious_patterns:

        if pattern in answer_clean:

            suspicious_matches += 1

    # =====================================================
    # SENTENCE ANALYSIS
    # =====================================================
    sentences = split_sentences(answer_clean)

    repeated_sentences = check_repetition(sentences)

    # =====================================================
    # LARGE PARAGRAPH DETECTION
    # =====================================================
    large_paragraph = False

    paragraphs = answer.split("\n")

    for para in paragraphs:

        if len(para.split()) > 120:

            large_paragraph = True

    # =====================================================
    # MASSIVE CONTENT DUMP
    # =====================================================
    word_count = len(answer_clean.split())

    content_dump_score = 0

    if word_count > 700:

        content_dump_score += 25

    elif word_count > 500:

        content_dump_score += 15

    # =====================================================
    # NUMBERED COPY DETECTION
    # =====================================================
    numbered_points = len(

        re.findall(r"\d+\.", answer)
    )

    numbered_score = 0

    if numbered_points >= 8:

        numbered_score += 15

    elif numbered_points >= 5:

        numbered_score += 8

    # =====================================================
    # POLISHED AI LANGUAGE
    # =====================================================
    polished_words = [

        "therefore",
        "thus",
        "hence",
        "moreover",
        "furthermore",
        "significantly",
        "remarkably",
        "consequently",
        "collectively",
        "transformed",
        "sophisticated",
        "monumental",
        "artistic excellence",
        "cultural richness",
        "engineering skills"
    ]

    polished_count = 0

    for word in polished_words:

        if word in answer_clean:

            polished_count += 1

    polished_score = 0

    if polished_count >= 5:

        polished_score += 15

    elif polished_count >= 3:

        polished_score += 8

    # =====================================================
    # STRUCTURE DETECTION
    # =====================================================
    structure_score = 0

    if "introduction" in answer_clean:

        structure_score += 5

    if "conclusion" in answer_clean:

        structure_score += 5

    if "body" in answer_clean:

        structure_score += 5

    # =====================================================
    # BULLET OVERUSE
    # =====================================================
    bullet_count = answer.count("•")

    bullet_score = 0

    if bullet_count > 15:

        bullet_score += 10

    elif bullet_count > 8:

        bullet_score += 5

    # =====================================================
    # TOPIC MISMATCH DETECTION
    # =====================================================
    mismatch_score = 0

    if keyword_ratio < 0.20:

        mismatch_score += 45

    elif keyword_ratio < 0.35:

        mismatch_score += 25

    # =====================================================
    # FINAL SCORE
    # =====================================================
    similarity_score = 0

    similarity_score += suspicious_matches * 10

    similarity_score += repeated_sentences * 10

    similarity_score += structure_score

    similarity_score += bullet_score

    similarity_score += polished_score

    similarity_score += content_dump_score

    similarity_score += numbered_score

    similarity_score += mismatch_score

    # =====================================================
    # LARGE PARAGRAPH PENALTY
    # =====================================================
    if large_paragraph:

        similarity_score += 15

    # =====================================================
    # LIMIT SCORE
    # =====================================================
    if similarity_score > 100:

        similarity_score = 100

    # =====================================================
    # FINAL STATUS
    # =====================================================
    if similarity_score >= 60:

        status = "Highly Suspicious"

    elif similarity_score >= 40:

        status = "Possibly Copied"

    elif similarity_score >= 20:

        status = "Moderate Similarity"

    else:

        status = "Original"

    # =====================================================
    # RETURN
    # =====================================================
    return {

        "similarity": similarity_score,

        "status": status
    }