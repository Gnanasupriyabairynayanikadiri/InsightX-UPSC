# =====================================================
# 📁 FILE: core/revision_engine.py
# SMART REVISION ENGINE
# =====================================================

import os
import json

from datetime import datetime, timedelta


# =====================================================
# STORAGE
# =====================================================

FILE = "storage/revisions.json"


# =====================================================
# ENSURE STORAGE
# =====================================================

def ensure_storage():

    os.makedirs(
        "storage",
        exist_ok=True
    )

    if not os.path.exists(FILE):

        with open(
            FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump({}, f)


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    ensure_storage()

    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

            return {}

    except:
        return {}


# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):

    ensure_storage()

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# ADD REVISION
# =====================================================

def add_revision(
    user,
    topic,
    subject="General"
):

    data = load_data()

    if user not in data:
        data[user] = []

    today = datetime.now()

    revision_plan = [

        1,
        3,
        7,
        15,
        30
    ]

    entries = []

    for day in revision_plan:

        revision_date = (

            today +
            timedelta(days=day)

        ).strftime("%Y-%m-%d")

        entries.append({

            "topic": topic,

            "subject": subject,

            "revision_date": revision_date,

            "completed": False
        })

    data[user].extend(entries)

    save_data(data)


# =====================================================
# GET DUE REVISIONS
# =====================================================

def get_due_revisions(user):

    data = load_data()

    revisions = data.get(user, [])

    today = datetime.now().strftime("%Y-%m-%d")

    due = []

    for item in revisions:

        if (

            item.get("revision_date") <= today
            and
            not item.get("completed", False)

        ):

            due.append(

                f"{item['topic']} ({item['subject']})"
            )

    return due


# =====================================================
# MARK REVISION COMPLETE
# =====================================================

def complete_revision(
    user,
    topic
):

    data = load_data()

    if user not in data:
        return

    for item in data[user]:

        if item["topic"] == topic:

            item["completed"] = True

    save_data(data)


# =====================================================
# GET ALL REVISIONS
# =====================================================

def get_all_revisions(user):

    data = load_data()

    return data.get(user, [])