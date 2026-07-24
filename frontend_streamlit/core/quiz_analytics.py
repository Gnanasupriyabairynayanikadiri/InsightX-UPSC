import json
import os

FILE = "storage/quiz_attempts.json"


def load_quiz_data():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FILE):

        with open(FILE, "w") as f:
            json.dump({}, f)

    with open(FILE, "r") as f:
        return json.load(f)


def save_quiz_data(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# =====================================================
# SAVE ATTEMPT
# =====================================================

def save_quiz_attempt(
    user,
    subject,
    chapter,
    score,
    total
):

    data = load_quiz_data()

    user = user.lower()

    data.setdefault(user, [])

    percentage = round(
        (score / total) * 100,
        2
    )

    data[user].append({

        "subject": subject,

        "chapter": chapter,

        "score": score,

        "total": total,

        "percentage": percentage

    })

    save_quiz_data(data)


# =====================================================
# QUIZ STATS
# =====================================================

def get_quiz_stats(user):

    data = load_quiz_data()

    user = user.lower()

    attempts = data.get(user, [])

    if not attempts:

        return {

            "attempts": 0,

            "average_score": 0,

            "highest_score": 0
        }

    percentages = [

        a["percentage"]

        for a in attempts
    ]

    return {

        "attempts": len(attempts),

        "average_score": round(
            sum(percentages) /
            len(percentages),
            2
        ),

        "highest_score": max(percentages)
    }


# =====================================================
# WEAK CHAPTERS
# =====================================================

def get_weak_chapters(user, threshold=50):

    data = load_quiz_data()

    attempts = data.get(user.lower(), [])

    weak = [
        a for a in attempts
        if a.get("percentage", 0) < threshold
    ]

    weak.sort(
        key=lambda x: x.get("percentage", 0)
    )

    return weak


# =====================================================
# STRONG CHAPTERS
# =====================================================

def get_strong_chapters(user, threshold=75):

    data = load_quiz_data()

    attempts = data.get(user.lower(), [])

    strong = [
        a for a in attempts
        if a.get("percentage", 0) >= threshold
    ]

    strong.sort(
        key=lambda x: x.get("percentage", 0),
        reverse=True
    )

    return strong

# =====================================================
# CHAPTER PERFORMANCE
# =====================================================

def get_chapter_performance(user):

    data = load_quiz_data()

    user = user.lower()

    attempts = data.get(user, [])

    performance = {}

    for attempt in attempts:

        key = (
            attempt.get("subject", ""),
            attempt.get("chapter", "")
        )

        if key not in performance:

            performance[key] = {
                "subject": attempt.get("subject", ""),
                "chapter": attempt.get("chapter", ""),
                "score": 0,
                "total": 0,
                "attempts": 0
            }

        performance[key]["score"] += attempt.get("score", 0)
        performance[key]["total"] += attempt.get("total", 0)
        performance[key]["attempts"] += 1

    result = []

    for item in performance.values():

        percentage = round(
            (item["score"] / item["total"]) * 100,
            2
        ) if item["total"] else 0

        result.append({
            "subject": item["subject"],
            "chapter": item["chapter"],
            "percentage": percentage,
            "attempts": item["attempts"]
        })

    return result