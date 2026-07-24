# =========================================================
# 📁 core/plagiarism.py (UPSC-GRADE FIXED VERSION)
# =========================================================

import re
import time
from difflib import SequenceMatcher


# =========================================================
# 🧠 TEXT NORMALIZATION
# =========================================================
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# =========================================================
# 🔍 COPY PASTE DETECTION (STRUCTURE + TEMPLATE)
# =========================================================
def detect_copy_paste(answer):

    text = normalize(answer)
    words = text.split()

    # -----------------------------------------------------
    # 1. VERY LARGE BLOCK WITHOUT BREAKS
    # -----------------------------------------------------
    if len(words) > 250 and "\n" not in answer:
        return {
            "flag": True,
            "reason": "Large pasted content detected"
        }

    # -----------------------------------------------------
    # 2. REPETITIVE PATTERN CHECK
    # -----------------------------------------------------
    repeated = re.findall(r"\b(\w+)\b(?:\s+\1\b){2,}", text)

    if repeated:
        return {
            "flag": True,
            "reason": "Highly repetitive word patterns detected"
        }

    # -----------------------------------------------------
    # 3. TEMPLATE STRUCTURE DETECTION (IMPORTANT FIX)
    # -----------------------------------------------------
    template_markers = [
        "introduction",
        "conclusion",
        "firstly",
        "secondly",
        "furthermore",
        "moreover",
        "in conclusion",
        "thus we can say",
        "it can be said that"
    ]

    match_count = sum(1 for t in template_markers if t in text)

    if len(words) > 120 and match_count >= 5:
        return {
            "flag": True,
            "reason": "Template-based structured answer detected"
        }

    return {
        "flag": False,
        "reason": ""
    }


# =========================================================
# 🧠 SEMANTIC SIMILARITY (ANTI-PARAPHRASE COPY)
# =========================================================
def semantic_similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


# =========================================================
# 🤖 AI-LIKE WRITING DETECTION (IMPROVED)
# =========================================================
def detect_ai_generated(answer):

    text = normalize(answer)

    ai_patterns = [
        "holistic approach",
        "multidimensional approach",
        "it is important to note",
        "in a broader sense",
        "can be seen as",
        "plays a crucial role",
        "comprehensive strategy",
        "balanced approach"
    ]

    score = sum(1 for p in ai_patterns if p in text)

    if score >= 3 and len(text.split()) > 120:
        return {
            "flag": True,
            "reason": "High likelihood of AI-generated structured answer"
        }

    return {
        "flag": False,
        "reason": ""
    }


# =========================================================
# ⏱ WRITING SPEED DETECTION
# =========================================================
def detect_suspicious_speed(answer, start_time):

    elapsed = max(time.time() - start_time, 0.001)

    words = len(answer.split())
    wpm = (words / elapsed) * 60

    if words > 150 and wpm > 200:
        return {
            "flag": True,
            "reason": "Suspiciously fast writing speed"
        }

    return {
        "flag": False,
        "reason": ""
    }


# =========================================================
# 🧠 MASTER PLAGIARISM CHECK ENGINE
# =========================================================
def plagiarism_check(answer, start_time, previous_answers=None):

    results = []

    # -----------------------------------------------------
    # COPY PASTE CHECK
    # -----------------------------------------------------
    cp = detect_copy_paste(answer)
    if cp["flag"]:
        results.append(cp["reason"])

    # -----------------------------------------------------
    # AI GENERATED CHECK
    # -----------------------------------------------------
    ai = detect_ai_generated(answer)
    if ai["flag"]:
        results.append(ai["reason"])

    # -----------------------------------------------------
    # SPEED CHECK
    # -----------------------------------------------------
    speed = detect_suspicious_speed(answer, start_time)
    if speed["flag"]:
        results.append(speed["reason"])

    # -----------------------------------------------------
    # SEMANTIC DUPLICATION CHECK (VERY IMPORTANT FIX)
    # -----------------------------------------------------
    if previous_answers:

        for past in previous_answers[-5:]:  # only last 5 for stability

            sim = semantic_similarity(answer, past)

            if sim > 0.75:
                results.append("High similarity with previous answers detected")
                break

    # -----------------------------------------------------
    # FINAL OUTPUT
    # -----------------------------------------------------
    return {
        "flagged": len(results) > 0,
        "issues": results,
        "risk_score": min(len(results) * 25, 100)  # optional scoring
    }