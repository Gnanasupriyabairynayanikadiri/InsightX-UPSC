# =========================================================
# FILE: core/answer_analytics.py
# ANSWER WRITING ANALYTICS ENGINE
# =========================================================

import json
import os
from datetime import datetime

ANSWER_FILE = "storage/answer_writing_attempts.json"


# =========================================================
# LOAD DATA
# =========================================================

def load_answer_data():

    if not os.path.exists(ANSWER_FILE):

        with open(ANSWER_FILE, "w") as f:
            json.dump({}, f)

    try:

        with open(ANSWER_FILE, "r") as f:
            return json.load(f)

    except:

        return {}


# =========================================================
# SAVE DATA
# =========================================================

def save_answer_data(data):

    with open(ANSWER_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


# =========================================================
# RECORD ANSWER ATTEMPT
# =========================================================

# =========================================================
# RECORD ANSWER ATTEMPT
# =========================================================

def record_answer_attempt(
    user,
    subject,
    chapter,
    level,
    score,
    out_of=15
):

    data = load_answer_data()

    user = str(user)

    if user not in data:
        data[user] = {}

    if subject not in data[user]:
        data[user][subject] = {}

    if chapter not in data[user][subject]:
        data[user][subject][chapter] = {}

    if level not in data[user][subject][chapter]:
        data[user][subject][chapter][level] = []

    percentage = round(
        (score / out_of) * 100,
        2
    ) if out_of else 0

    data[user][subject][chapter][level].append({

        "score": score,

        "out_of": out_of,

        "percentage": percentage,

        "date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    })

    save_answer_data(data)

# =========================================================
# OVERALL ANSWER WRITING STATS
# =========================================================

def get_answer_stats(user):

    data = load_answer_data()

    user_data = data.get(str(user), {})

    if not user_data:
        return {
            "attempts": 0,
            "average_score": 0,
            "highest_score": 0,
            "average_percentage": 0
        }

    attempts = 0
    total_score = 0
    total_possible = 0
    highest_score = 0

    for subject in user_data.values():

        for chapter in subject.values():

            for level_attempts in chapter.values():

                for attempt in level_attempts:

                    attempts += 1

                    score = attempt.get("score", 0)
                    out_of = attempt.get("out_of", 0)

                    total_score += score
                    total_possible += out_of

                    highest_score = max(
                        highest_score,
                        score
                    )

    return {
        "attempts": attempts,
        "average_score": round(total_score / attempts, 2) if attempts else 0,
        "highest_score": highest_score,
        "average_percentage": round((total_score / total_possible) * 100, 2)
        if total_possible else 0
    }


# =========================================================
# SUBJECT PERFORMANCE
# =========================================================

def get_subject_performance(user):

    data = load_answer_data()

    user_data = data.get(
        str(user),
        {}
    )

    performance = []

    for subject_name, subject in user_data.items():

        for chapter_name, chapter in subject.items():

            total_score = 0
            total_possible = 0
            attempts_count = 0

            for level_name, level_attempts in chapter.items():

                for attempt in level_attempts:

                    attempts_count += 1

                    total_score += attempt.get(
                        "score",
                        0
                    )

                    total_possible += attempt.get(
                        "out_of",
                        0
                    )

            percentage = round(
                (total_score / total_possible) * 100,
                2
            ) if total_possible else 0

            performance.append({

                "subject": subject_name,
                "chapter": chapter_name,
                "attempts": attempts_count,
                "percentage": percentage
            })

    return performance


# =========================================================
# CHAPTER PERFORMANCE
# =========================================================

def get_chapter_performance(user):

    data = load_answer_data()

    user_data = data.get(
        str(user),
        {}
    )

    performance = []

    for subject_name, subject in user_data.items():

        for chapter_name, chapter in subject.items():

            total_score = 0
            total_possible = 0
            attempts_count = 0

            for level_attempts in chapter.values():

                for attempt in level_attempts:

                    attempts_count += 1
                    total_score += attempt["score"]
                    total_possible += attempt["out_of"]

            percentage = round(
                (total_score / total_possible) * 100,
                2
            ) if total_possible else 0

            performance.append({

                "subject": subject_name,
                "chapter": chapter_name,
                "percentage": percentage,
                "attempts": attempts_count
            })
    return performance

# =========================================================
# WEAK TOPICS
# =========================================================

def get_weak_topics(user, limit=5):

    chapters = get_chapter_performance(user)

    chapters.sort(
        key=lambda x: x["percentage"]
    )

    return chapters[:limit]


# =========================================================
# STRONG TOPICS
# =========================================================

def get_strong_topics(user, limit=5):

    chapters = get_chapter_performance(user)

    chapters.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return chapters[:limit]


# =========================================================
# RECENT ANSWERS
# =========================================================

def get_recent_answers(
    user,
    limit=10
):

    data = load_answer_data()

    user_data = data.get(
        str(user),
        {}
    )

    recent = []

    for subject_name, subject in user_data.items():

        for chapter_name, chapter in subject.items():

            for level_name, level_attempts in chapter.items():

                for attempt in level_attempts:

                    recent.append({

                        "subject": subject_name,

                        "chapter": chapter_name,

                        "level": level_name,

                        "score": attempt.get("score", 0),

                        "out_of": attempt.get("out_of", 0),

                        "date": attempt.get("date", "")
                    })

    recent.sort(
        key=lambda x:
        x["date"],
        reverse=True
    )

    return recent[:limit]

def get_level_performance(user):

    data = load_answer_data()

    user_data = data.get(
        str(user),
        {}
    )

    result = []

    for subject_name, subject in user_data.items():

        for chapter_name, chapter in subject.items():

            for level_name, attempts in chapter.items():

                total_score = sum(
                    x["score"]
                    for x in attempts
                )

                total_possible = sum(
                    x["out_of"]
                    for x in attempts
                )

                percentage = round(
                    (
                        total_score /
                        total_possible
                    ) * 100,
                    2
                ) if total_possible else 0

                result.append({

                    "subject": subject_name,

                    "chapter": chapter_name,

                    "level": level_name,

                    "percentage": percentage
                })

    return result