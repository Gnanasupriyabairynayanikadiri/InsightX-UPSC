# =========================================
# 📁 core/history.py (FIXED VERSION)
# =========================================

import os
import json
from datetime import datetime

FILE = "storage/daily_answers.json"


# =========================================
# STORAGE SETUP
# =========================================
def ensure_storage():
    os.makedirs("storage", exist_ok=True)


def load_answers():
    ensure_storage()

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_answers(data):
    ensure_storage()

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================================
# USER NORMALIZATION (IMPORTANT FIX)
# =========================================
def normalize(user):
    return str(user).strip().lower()


# =========================================
# GET USER ANSWERS
# =========================================
def get_user_answers(user):

    data = load_answers()
    user = normalize(user)

    return data.get(user, [])


# =========================================
# SAVE USER ANSWER (UPGRADED)
# =========================================
def save_user_answer(user, answer_data):

    data = load_answers()
    user = normalize(user)

    if user not in data:
        data[user] = []

    # =====================================
    # ENRICH DATA (CRITICAL FIX)
    # =====================================
    enriched = {
        "question": answer_data.get("question", ""),
        "answer": answer_data.get("answer", ""),
        "score": answer_data.get("score", 0),
        "subject": answer_data.get("subject", ""),
        "category": answer_data.get("category", ""),
        "chapter": answer_data.get("chapter", ""),
        "level": answer_data.get("level", ""),
        "topic_keywords": answer_data.get("topic_keywords", []),
        "copy_paste_flag": answer_data.get("copy_paste_flag", False),
        "word_count": len(answer_data.get("answer", "").split()),
        "timestamp": datetime.now().isoformat()
    }

    # =====================================
    # DUPLICATE PREVENTION (SAFE)
    # =====================================
    for item in data[user]:
        if (
            item.get("question") == enriched["question"]
            and item.get("answer") == enriched["answer"]
        ):
            return  # skip duplicate

    data[user].append(enriched)

    save_answers(data)