# =========================================================
# 📁 core/progress.py
# FULL FIXED + STABLE VERSION
# =========================================================

import json
import os

# =========================================================
# STORAGE FILE
# =========================================================
FILE = "storage/progress.json"


# =========================================================
# STORAGE HELPERS
# =========================================================
def ensure_storage():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FILE):

        with open(FILE, "w", encoding="utf-8") as f:

            json.dump({}, f)


def load_data():

    ensure_storage()

    try:

        with open(FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception:

        return {}


def save_data(data):

    ensure_storage()

    with open(FILE, "w", encoding="utf-8") as f:

        json.dump(

            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# NORMALIZATION
# =========================================================
def normalize(value):

    return str(value).strip().lower()


# =========================================================
# INIT USER
# =========================================================
def init_user(user):

    data = load_data()

    user = normalize(user)

    if user not in data:

        data[user] = {

            "chapters": {},

            "levels": {},

            "mains": {},

            "bookmarks": [],

            "resume": {}
        }

        save_data(data)

    return data


# =========================================================
# CHAPTER COMPLETION
# =========================================================
def mark_completed(

    user,
    subject,
    cls,
    chapter
):

    data = init_user(user)

    user = normalize(user)

    subject = normalize(subject)

    cls = normalize(cls)

    chapter = normalize(chapter)

    data[user]["chapters"].setdefault(subject, {})

    data[user]["chapters"][subject].setdefault(cls, [])

    if chapter not in data[user]["chapters"][subject][cls]:

        data[user]["chapters"][subject][cls].append(chapter)

    save_data(data)


def is_completed(

    user,
    subject,
    cls,
    chapter
):

    data = load_data()

    user = normalize(user)

    subject = normalize(subject)

    cls = normalize(cls)

    chapter = normalize(chapter)

    return chapter in (

        data.get(user, {})

        .get("chapters", {})

        .get(subject, {})

        .get(cls, [])
    )


# =========================================================
# MCQ LEVEL PROGRESS
# =========================================================
def mark_level_completed(

    user,
    subject,
    topic,
    level
):

    data = init_user(user)

    user = normalize(user)

    subject = normalize(subject)

    topic = normalize(topic)

    level = normalize(level)

    data[user]["levels"].setdefault(subject, {})

    data[user]["levels"][subject].setdefault(topic, [])

    if level not in data[user]["levels"][subject][topic]:

        data[user]["levels"][subject][topic].append(level)

    save_data(data)


def is_level_completed(

    user,
    subject,
    topic,
    level
):

    data = load_data()

    user = normalize(user)

    subject = normalize(subject)

    topic = normalize(topic)

    level = normalize(level)

    return level in (

        data.get(user, {})

        .get("levels", {})

        .get(subject, {})

        .get(topic, [])
    )


def get_level_progress(

    user,
    subject,
    topic
):

    data = load_data()

    user = normalize(user)

    subject = normalize(subject)

    topic = normalize(topic)

    completed = (

        data.get(user, {})

        .get("levels", {})

        .get(subject, {})

        .get(topic, [])
    )

    return {

        "basic": "basic" in completed,

        "moderate": "moderate" in completed,

        "advanced": "advanced" in completed
    }


# =========================================================
# MAINS PROGRESS
# =========================================================
def mark_mains_completed(

    user,
    subject,
    chapter,
    level
):

    data = init_user(user)

    user = normalize(user)

    subject = normalize(subject)

    chapter = normalize(chapter)

    level = normalize(level)

    data[user]["mains"].setdefault(subject, {})

    data[user]["mains"][subject].setdefault(chapter, [])

    if level not in data[user]["mains"][subject][chapter]:

        data[user]["mains"][subject][chapter].append(level)

    save_data(data)


def is_mains_completed(

    user,
    subject,
    chapter,
    level
):

    data = load_data()

    user = normalize(user)

    subject = normalize(subject)

    chapter = normalize(chapter)

    level = normalize(level)

    return level in (

        data.get(user, {})

        .get("mains", {})

        .get(subject, {})

        .get(chapter, [])
    )


def get_mains_progress(

    user,
    subject,
    chapter
):

    data = load_data()

    user = normalize(user)

    subject = normalize(subject)

    chapter = normalize(chapter)

    completed = (

        data.get(user, {})

        .get("mains", {})

        .get(subject, {})

        .get(chapter, [])
    )

    return {

        "basic": "basic" in completed,

        "moderate": "moderate" in completed,

        "advanced": "advanced" in completed
    }



# =========================================================
# DETAILED DASHBOARD PROGRESS
# =========================================================
def get_detailed_progress(

    user,
    syllabus_data
):

    data = load_data()

    user = normalize(user)

    total = 0

    completed = 0

    subject_progress = {}

    for subject in syllabus_data:

        subject_key = normalize(subject)

        subject_total = 0

        subject_done = 0

        for cls in syllabus_data[subject]:

            cls_key = normalize(cls)

            chapters = syllabus_data[subject][cls]

            subject_total += len(chapters)

            completed_chapters = (

                data.get(user, {})

                .get("chapters", {})

                .get(subject_key, {})

                .get(cls_key, [])
            )

            subject_done += len(completed_chapters)

        percentage = int(

            (subject_done / subject_total) * 100

        ) if subject_total else 0

        subject_progress[subject] = {

            "done": subject_done,

            "total": subject_total,

            "percent": percentage
        }

        total += subject_total

        completed += subject_done

    overall = int(

        (completed / total) * 100

    ) if total else 0

    return {

        "overall": overall,

        "total": total,

        "done": completed,

        "subjects": subject_progress
    }


# =========================================================
# OVERALL USER STATS
# =========================================================
def get_overall_stats(user):

    data = load_data()

    user = normalize(user)

    user_data = data.get(user, {})

    mcq_completed = sum(

        len(v)

        for subject in user_data.get("levels", {}).values()

        for v in subject.values()
    )

    mains_completed = sum(

        len(v)

        for subject in user_data.get("mains", {}).values()

        for v in subject.values()
    )


    return {

        "mcq_levels_completed": mcq_completed,

        "mains_levels_completed": mains_completed,

        "bookmarks": len(

            user_data.get("bookmarks", [])
        )
    }