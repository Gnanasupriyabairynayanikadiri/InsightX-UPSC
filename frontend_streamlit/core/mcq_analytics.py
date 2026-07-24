# =========================================================
# FILE: core/mcq_analytics.py
# MCQ ANALYTICS ENGINE
# =========================================================

import json
import os
from datetime import datetime

MCQ_FILE = "storage/mcq_attempts.json"


# =========================================================
# LOAD DATA
# =========================================================

def load_mcq_data():

    if not os.path.exists(MCQ_FILE):

        with open(MCQ_FILE, "w") as f:
            json.dump({}, f)

    try:

        with open(MCQ_FILE, "r") as f:
            return json.load(f)

    except:

        return {}


# =========================================================
# SAVE DATA
# =========================================================

def save_mcq_data(data):

    with open(MCQ_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


# =========================================================
# RECORD MCQ ATTEMPT
# =========================================================

def record_mcq_attempt(
    user,
    subject,
    chapter,
    topic,
    level,
    correct,
    total
):

    data = load_mcq_data()

    user = str(user)

    if user not in data:
        data[user] = {}

    if subject not in data[user]:
        data[user][subject] = {}

    if chapter not in data[user][subject]:
        data[user][subject][chapter] = {}

    if topic not in data[user][subject][chapter]:
        data[user][subject][chapter][topic] = {}

    if level not in data[user][subject][chapter][topic]:
        data[user][subject][chapter][topic][level] = []

    percentage = round(
        (correct / total) * 100,
        2
    ) if total else 0

    data[user][subject][chapter][topic][level].append({

        "correct": correct,
        "total": total,
        "percentage": percentage,

        "date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    })

    save_mcq_data(data)

# =========================================================
# OVERALL MCQ STATS
# =========================================================

def get_mcq_stats(user):

    data = load_mcq_data()

    user_data = data.get(
        str(user),
        {}
    )

    attempts = 0
    total_correct = 0
    total_questions = 0
    highest = 0

    for subject in user_data.values():

        for chapter in subject.values():

            for topic in chapter.values():

                for level_attempts in topic.values():

                    for attempt in level_attempts:

                        attempts += 1

                        total_correct += attempt.get(
                            "correct",
                            0
                        )

                        total_questions += attempt.get(
                            "total",
                            0
                        )

                        highest = max(
                            highest,
                            attempt.get(
                                "percentage",
                                0
                            )
                        )

    average = round(
        (
            total_correct /
            total_questions
        ) * 100,
        2
    ) if total_questions else 0

    return {

        "attempts":
            attempts,

        "correct":
            total_correct,

        "questions":
            total_questions,

        "average_accuracy":
            average,

        "highest_accuracy":
            highest
    }

# =========================================================
# TOPIC PERFORMANCE
# =========================================================

def get_topic_performance(user):

    data = load_mcq_data()

    user_data = data.get(
        str(user),
        {}
    )

    performance = []

    for subject_name, subjects in user_data.items():

        for chapter_name, chapters in subjects.items():

            for topic_name, topics in chapters.items():

                total_correct = 0
                total_questions = 0
                attempts_count = 0

                for level_name, level_attempts in topics.items():

                    for item in level_attempts:

                        attempts_count += 1

                        total_correct += item.get(
                            "correct",
                            0
                        )

                        total_questions += item.get(
                            "total",
                            0
                        )

                accuracy = round(
                    (
                        total_correct /
                        total_questions
                    ) * 100,
                    2
                ) if total_questions else 0

                performance.append({

                    "subject":
                        subject_name,

                    "chapter":
                        chapter_name,

                    "topic":
                        topic_name,

                    "accuracy":
                        accuracy,

                    "attempts":
                        attempts_count
                })

    return performance


# =========================================================
# STRONG TOPICS
# =========================================================

def get_strong_topics(
    user,
    limit=5
):
    topics = get_topic_performance(user)

    topics.sort(
        key=lambda x: x["accuracy"],
        reverse=True
    )

    return topics[:limit]


# =========================================================
# WEAK TOPICS
# =========================================================
def get_weak_topics(
    user,
    limit=5
):
    topics = get_topic_performance(user)

    topics.sort(
        key=lambda x: x["accuracy"]
    )

    return topics[:limit]


# =========================================================
# LEVEL ANALYTICS
# =========================================================

def get_level_stats(
    user,
    subject,
    chapter,
    topic
):

    data = load_mcq_data()

    topic_data = (
        data.get(str(user), {})
        .get(subject, {})
        .get(chapter, {})
        .get(topic, {})
    )

    levels = {

        "basic": {
            "attempts": 0,
            "best": 0
        },

        "moderate": {
            "attempts": 0,
            "best": 0
        },

        "advanced": {
            "attempts": 0,
            "best": 0
        }
    }

    for level_name, attempts in topic_data.items():

        key = level_name.lower()

        if key not in levels:
            continue

        levels[key]["attempts"] = len(attempts)

        levels[key]["best"] = max(
            [x.get("percentage", 0) for x in attempts],
            default=0
        )

    return levels

