# =========================================================
# 📁 FILE: core/bookmark_engine.py
# PERSISTENT BOOKMARK SYSTEM (FIXED + STABLE)
# =========================================================

import os
import json


# =========================================================
# STORAGE FILE
# =========================================================
BOOKMARK_FILE = "storage/bookmarks.json"


# =========================================================
# NORMALIZER (CRITICAL FIX)
# =========================================================
def norm(x):
    return str(x).strip().lower()


# =========================================================
# ENSURE STORAGE
# =========================================================
def ensure_storage():

    os.makedirs("storage", exist_ok=True)

    if not os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "w") as f:
            json.dump({}, f)


# =========================================================
# LOAD
# =========================================================
def load_bookmarks():

    ensure_storage()

    try:
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# =========================================================
# SAVE
# =========================================================
def save_bookmarks(data):

    ensure_storage()

    with open(BOOKMARK_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================================================
# ADD BOOKMARK
# =========================================================
def add_bookmark(
    user,
    subject,
    category,
    chapter,
    topic,
    topic_index
):

    data = load_bookmarks()

    user = norm(user)

    if user not in data:
        data[user] = []

    new_item = {
        "subject": subject,
        "category": category,
        "chapter": chapter,
        "topic": topic,
        "topic_index": topic_index
    }

    # =====================================================
    # PREVENT DUPLICATES (FIXED COMPARISON)
    # =====================================================
    exists = any(
        norm(b["subject"]) == norm(subject) and
        norm(b["chapter"]) == norm(chapter) and
        norm(b["topic"]) == norm(topic)
        for b in data[user]
    )

    if exists:
        return False

    data[user].append(new_item)

    save_bookmarks(data)

    return True


# =========================================================
# GET USER BOOKMARKS
# =========================================================
def get_user_bookmarks(user):

    data = load_bookmarks()

    return data.get(norm(user), [])


# =========================================================
# REMOVE BOOKMARK (FIXED MATCHING LOGIC)
# =========================================================
def remove_bookmark(
    user,
    subject,
    chapter,
    topic
):

    data = load_bookmarks()

    user = norm(user)

    if user not in data:
        return False

    data[user] = [
        b for b in data[user]
        if not (
            norm(b.get("subject")) == norm(subject) and
            norm(b.get("chapter")) == norm(chapter) and
            norm(b.get("topic")) == norm(topic)
        )
    ]

    save_bookmarks(data)

    return True


# =========================================================
# CLEAR ALL BOOKMARKS (OPTIONAL UTILITY)
# =========================================================
def clear_user_bookmarks(user):

    data = load_bookmarks()

    user = norm(user)

    if user in data:
        data[user] = []

    save_bookmarks(data)