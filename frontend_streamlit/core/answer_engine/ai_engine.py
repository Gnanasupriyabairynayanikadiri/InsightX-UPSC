import random
from difflib import SequenceMatcher


# =========================================================
# 1. QUESTION - ANSWER MATCH SCORE
# =========================================================
def match_score(question, answer):

    q = set(question.lower().split())
    a = set(answer.lower().split())

    if not q:
        return 0

    return len(q.intersection(a)) / len(q)


# =========================================================
# 2. COPY PASTE DETECTOR
# =========================================================
def detect_copy_paste(answer):

    text = answer.lower()

    template_patterns = [
        "introduction",
        "conclusion",
        "however",
        "therefore",
        "furthermore",
        "thus the vijayanagara",
        "the gupta period is",
        "the harappan civilization"
    ]

    hits = sum(1 for p in template_patterns if p in text)

    if hits >= 5:
        return True, "Template-based answer detected"

    return False, "Original answer"


# =========================================================
# 3. STRUCTURE ANALYSIS
# =========================================================
def structure_score(answer):

    text = answer.lower()

    score = 0

    if "introduction" in text:
        score += 1

    if "conclusion" in text:
        score += 1

    if "example" in text:
        score += 1

    if "however" in text or "therefore" in text:
        score += 1

    return score


# =========================================================
# 4. CONTENT DEPTH ANALYSIS
# =========================================================
def depth_score(answer):

    keywords = [
        "impact", "cause", "reason", "analysis",
        "government", "policy", "society",
        "culture", "economy", "environment"
    ]

    text = answer.lower()

    return sum(1 for k in keywords if k in text)


# =========================================================
# 5. FINAL AI SCORE ENGINE
# =========================================================
def evaluate_answer_ai(question, answer, marks=10):

    if not answer.strip():
        return {
            "score": 0,
            "feedback": ["No answer provided."]
        }

    words = len(answer.split())

    match = match_score(question, answer)
    structure = structure_score(answer)
    depth = depth_score(answer)

    score = 0
    feedback = []

    # =====================================================
    # RELEVANCE (MOST IMPORTANT)
    # =====================================================
    if match > 0.5:
        score += 3
        feedback.append("Good relevance to question.")

    elif match > 0.3:
        score += 2
        feedback.append("Partial relevance. Improve focus.")

    else:
        score += 1
        feedback.append("Low relevance to question.")

    # =====================================================
    # STRUCTURE
    # =====================================================
    if structure >= 3:
        score += 3
        feedback.append("Well-structured answer.")

    elif structure == 2:
        score += 2
        feedback.append("Basic structure present.")

    else:
        score += 1
        feedback.append("Improve structure (Intro/Conclusion).")

    # =====================================================
    # DEPTH
    # =====================================================
    if depth >= 4:
        score += 3
        feedback.append("Good analytical depth.")

    elif depth >= 2:
        score += 2
        feedback.append("Moderate analysis.")

    else:
        feedback.append("Add more analytical dimensions.")

    # =====================================================
    # LENGTH CHECK
    # =====================================================
    if 120 <= words <= 250:
        score += 1
        feedback.append("Good answer length.")

    elif words < 100:
        feedback.append("Answer is too short.")

    else:
        feedback.append("Try to be more concise.")

    # =====================================================
    # COPY PASTE DETECTION
    # =====================================================
    copy, reason = detect_copy_paste(answer)

    if copy:
        score -= 2
        feedback.append(f"⚠️ Copy-paste detected: {reason}")

    # =====================================================
    # FINAL SCORE LIMIT
    # =====================================================
    score = max(0, min(score, 10))

    # =====================================================
    # UPSC RANDOM FEEDBACK BOOST
    # =====================================================
    bonus = [
        "Add committee/reports for enrichment.",
        "Use constitutional or historical terms.",
        "Improve conclusion strength.",
        "Include examples for better marks.",
        "Link with current affairs."
    ]

    feedback.append(random.choice(bonus))

    return {
        "score": score,
        "feedback": feedback,
        "match_score": round(match, 2),
        "structure_score": structure,
        "depth_score": depth
    }