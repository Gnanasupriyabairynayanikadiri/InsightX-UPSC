# =========================================================
# 📁 FILE: core/analytics.py
# =========================================================

import os
import json
from collections import defaultdict

from core.xp import (
    get_xp,
    get_rank,
    get_streak
)


# =========================================================
# STORAGE
# =========================================================
ANSWER_FILE = "storage/daily_answers.json"


# =========================================================
# SAFE USER NORMALIZATION (IMPORTANT FIX)
# =========================================================
def normalize_user(user):

    if not user:
        return "guest"

    return str(user).strip().lower()


# =========================================================
# LOAD ANSWERS
# =========================================================
def load_answers():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(ANSWER_FILE):
        return {}

    try:
        with open(ANSWER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, dict) else {}

    except Exception:
        return {}


# =========================================================
# GET USER ANSWERS
# =========================================================
def get_user_answers(user):

    user = normalize_user(user)

    data = load_answers()

    answers = data.get(user, [])

    return answers if isinstance(answers, list) else []


# =========================================================
# TOTAL ANSWERS
# =========================================================
def total_answers_written(user):

    return len(get_user_answers(user))


# =========================================================
# SAFE SCORE EXTRACTOR
# =========================================================
def _extract_scores(answers):

    scores = []

    for a in answers:

        try:
            score = a.get("score", 0)

            if isinstance(score, (int, float)):
                scores.append(score)

        except Exception:
            continue

    return scores


# =========================================================
# AVERAGE SCORE
# =========================================================
def average_score(user):

    scores = _extract_scores(get_user_answers(user))

    if not scores:
        return 0

    return round(sum(scores) / len(scores), 2)


# =========================================================
# HIGHEST SCORE
# =========================================================
def highest_score(user):

    scores = _extract_scores(get_user_answers(user))

    return max(scores) if scores else 0


# =========================================================
# LOWEST SCORE
# =========================================================
def lowest_score(user):

    scores = _extract_scores(get_user_answers(user))

    return min(scores) if scores else 0


# =========================================================
# SUBJECT WISE ANALYTICS
# =========================================================
def subject_wise_scores(user):

    answers = get_user_answers(user)

    subjects = defaultdict(list)

    for a in answers:

        subject = a.get("subject") or "Unknown"

        try:
            score = a.get("score", 0)

            if isinstance(score, (int, float)):
                subjects[subject].append(score)

        except Exception:
            continue

    result = {}

    for subject, scores in subjects.items():

        if not scores:
            continue

        result[subject] = {
            "average": round(sum(scores) / len(scores), 2),
            "attempts": len(scores),
            "highest": max(scores),
            "lowest": min(scores)
        }

    return result


# =========================================================
# STRONGEST SUBJECT
# =========================================================
def strongest_subject(user):

    data = subject_wise_scores(user)

    if not data:
        return None

    return max(data, key=lambda s: data[s]["average"])


# =========================================================
# WEAKEST SUBJECT
# =========================================================
def weakest_subject(user):

    data = subject_wise_scores(user)

    if not data:
        return None

    return min(data, key=lambda s: data[s]["average"])


# =========================================================
# IMPROVEMENT TREND (FIXED STABILITY)
# =========================================================
def improvement_trend(user):

    scores = _extract_scores(get_user_answers(user))

    if len(scores) < 6:
        return {"improved": False, "difference": 0}

    mid = len(scores) // 2

    first_half = scores[:mid]
    second_half = scores[mid:]

    if not first_half or not second_half:
        return {"improved": False, "difference": 0}

    avg1 = sum(first_half) / len(first_half)
    avg2 = sum(second_half) / len(second_half)

    diff = round(avg2 - avg1, 2)

    return {
        "improved": diff > 0,
        "difference": diff
    }


# =========================================================
# RECENT PERFORMANCE
# =========================================================
def recent_performance(user, limit=5):

    answers = get_user_answers(user)

    return list(reversed(answers[-limit:]))


# =========================================================
# SCORE DISTRIBUTION
# =========================================================
def score_distribution(user):

    answers = get_user_answers(user)

    distribution = {
        "0-3": 0,
        "4-5": 0,
        "6-7": 0,
        "8-10": 0
    }

    for a in answers:

        score = a.get("score", 0)

        if score <= 3:
            distribution["0-3"] += 1
        elif score <= 5:
            distribution["4-5"] += 1
        elif score <= 7:
            distribution["6-7"] += 1
        else:
            distribution["8-10"] += 1

    return distribution


# =========================================================
# FULL ANALYTICS ENGINE
# =========================================================
def get_full_analytics(user):

    return {
        "total_answers": total_answers_written(user),
        "average_score": average_score(user),
        "highest_score": highest_score(user),
        "lowest_score": lowest_score(user),

        "strongest_subject": strongest_subject(user),
        "weakest_subject": weakest_subject(user),
        "subject_wise": subject_wise_scores(user),

        "improvement": improvement_trend(user),
        "distribution": score_distribution(user),
        "recent": recent_performance(user),

        "xp": get_xp(user),
        "rank": get_rank(user),
        "streak": get_streak(user)
    }


# =========================================================
# PERFORMANCE LABEL
# =========================================================
def performance_label(avg):

    if avg >= 8:
        return "🏆 Excellent"
    elif avg >= 6:
        return "🔥 Good"
    elif avg >= 4:
        return "📘 Average"
    else:
        return "⚠️ Needs Improvement"


# =========================================================
# USER SUMMARY (DASHBOARD READY)
# =========================================================
def get_user_summary(user):

    analytics = get_full_analytics(user)

    avg = analytics["average_score"]

    return {
        "answers": analytics["total_answers"],
        "average": avg,
        "label": performance_label(avg),
        "rank": analytics["rank"],
        "xp": analytics["xp"],
        "streak": analytics["streak"],
        "best_subject": analytics["strongest_subject"],
        "weak_subject": analytics["weakest_subject"]
    }