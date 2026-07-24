# =========================================================
# 🧠 UPSC MCQ ENGINE (CORE LOGIC ONLY)
# =========================================================

import os
import json
from datetime import date

# =========================================================
# STORAGE FILE
# =========================================================

FILE = "storage/mcq_data.json"


# =========================================================
# SAFE STORAGE INIT
# =========================================================

def ensure_storage():
    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    ensure_storage()

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, dict) else {}

    except:
        return {}


# =========================================================
# SAVE DATA
# =========================================================

def save_data(data):
    ensure_storage()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================================================
# NORMALIZE USER
# =========================================================

def normalize_user(user):
    if not user:
        return "guest"
    return str(user).strip().lower()


# =========================================================
# ADD MCQ ATTEMPT
# =========================================================

def add_mcq_attempt(user, question, selected_option, correct_option, subject="General"):
    """
    Stores MCQ attempt with scoring logic
    """

    user = normalize_user(user)
    data = load_data()

    if user not in data:
        data[user] = []

    is_correct = selected_option == correct_option

    entry = {
        "date": str(date.today()),
        "subject": subject,
        "question": question,
        "selected_option": selected_option,
        "correct_option": correct_option,
        "is_correct": is_correct,
        "score": 1 if is_correct else 0
    }

    data[user].append(entry)
    save_data(data)

    return is_correct


# =========================================================
# GET USER MCQS
# =========================================================

def get_user_mcqs(user):
    user = normalize_user(user)
    data = load_data()
    return data.get(user, [])


# =========================================================
# MCQ STATS
# =========================================================

def mcq_stats(user):

    mcqs = get_user_mcqs(user)

    if not mcqs:
        return {
            "total": 0,
            "correct": 0,
            "accuracy": 0
        }

    total = len(mcqs)
    correct = sum(1 for m in mcqs if m.get("is_correct"))

    accuracy = round((correct / total) * 100, 2)

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy
    }


# =========================================================
# SUBJECT WISE PERFORMANCE
# =========================================================

def subject_wise_mcq(user):

    mcqs = get_user_mcqs(user)

    subjects = {}

    for m in mcqs:

        subject = m.get("subject", "General")

        if subject not in subjects:
            subjects[subject] = {
                "total": 0,
                "correct": 0
            }

        subjects[subject]["total"] += 1

        if m.get("is_correct"):
            subjects[subject]["correct"] += 1

    # calculate accuracy
    for subject in subjects:
        t = subjects[subject]["total"]
        c = subjects[subject]["correct"]

        subjects[subject]["accuracy"] = round((c / t) * 100, 2) if t else 0

    return subjects


# =========================================================
# WEAK SUBJECT IDENTIFICATION
# =========================================================

def weakest_subject(user):

    data = subject_wise_mcq(user)

    if not data:
        return None

    return min(data.items(), key=lambda x: x[1]["accuracy"])[0]


# =========================================================
# STRONGEST SUBJECT
# =========================================================

def strongest_subject(user):

    data = subject_wise_mcq(user)

    if not data:
        return None

    return max(data.items(), key=lambda x: x[1]["accuracy"])[0]


# =========================================================
# RECENT ATTEMPTS
# =========================================================

def recent_mcqs(user, limit=10):

    mcqs = get_user_mcqs(user)

    return mcqs[-limit:][::-1]


# =========================================================
# CLEAR DATA (OPTIONAL RESET)
# =========================================================

def reset_mcq_data(user):

    user = normalize_user(user)
    data = load_data()

    if user in data:
        data[user] = []
        save_data(data)
        return True

    return False