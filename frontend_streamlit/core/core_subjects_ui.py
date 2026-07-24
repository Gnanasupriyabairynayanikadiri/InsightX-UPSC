# =========================================================
# 📁 FILE: core/core_subjects_ui.py
# FINAL UPSC-GRADED VERSION (LOCK + BOOKMARK + MCQ PROGRESSION)
# =========================================================

import streamlit as st
import re
import json
import os

from core.state_manager import init_state
from core.loader import load_subjects
from core.mcq_analytics import record_mcq_attempt

# =========================================================
# USER NORMALIZER
# =========================================================
def normalize_user(user):
    return "guest" if not user else str(user).strip().lower()


# =========================================================
# STORAGE
# =========================================================
BOOKMARK_FILE = "storage/bookmarks.json"


def ensure_storage():
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, "w") as f:
            json.dump({}, f)


def load_bookmarks():
    ensure_storage()
    try:
        with open(BOOKMARK_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_bookmarks(data):
    ensure_storage()
    with open(BOOKMARK_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================================================
# BOOKMARK FUNCTIONS (RESTORED)
# =========================================================
def add_bookmark(user, subject, category, chapter, topic, idx):
    user = normalize_user(user)
    data = load_bookmarks()

    data.setdefault(user, [])

    for b in data[user]:
        if b["subject"] == subject and b["topic"] == topic:
            return False

    data[user].append({
        "subject": subject,
        "category": category,
        "chapter": chapter,
        "topic": topic,
        "index": idx
    })

    save_bookmarks(data)
    return True


def get_bookmarks(user):
    user = normalize_user(user)
    return load_bookmarks().get(user, [])


# =========================================================
# MCQ LEVEL UNLOCK SYSTEM (🔥 NEW CORE LOGIC)
# =========================================================
def get_unlocked_level(progress):
    """
    progress example:
    {
        "basic": True,
        "moderate": False,
        "advanced": False
    }
    """
    if not progress.get("basic"):
        return "basic"
    if not progress.get("moderate"):
        return "moderate"
    return "advanced"


def mark_level_complete(progress, level):
    progress[level] = True
    return progress


# =========================================================
# MCQ RENDERER (LOCKED SYSTEM)
# =========================================================
def render_mcqs(
    user,
    subject,
    chapter,
    mcqs
):

    if not mcqs:
        return

    st.markdown("## 🧠 Practice MCQs")

    progress_key = f"{subject}_{chapter}_mcq_progress"

    if progress_key not in st.session_state:

        st.session_state[progress_key] = {
            "basic": False,
            "moderate": False,
            "advanced": False
        }

    progress = st.session_state[progress_key]

    levels = [
        "basic",
        "moderate",
        "advanced"
    ]

    for idx, level in enumerate(levels):

        questions = mcqs.get(level, [])

        if not questions:
            continue

        # ---------------------------------
        # LOCK SYSTEM
        # ---------------------------------

        unlocked = False

        if level == "basic":
            unlocked = True

        elif level == "moderate":
            unlocked = progress["basic"]

        elif level == "advanced":
            unlocked = progress["moderate"]

        if not unlocked:

            st.warning(
                f"🔒 {level.capitalize()} Locked — Complete previous level"
            )

            continue

        st.subheader(
            f"📊 {level.capitalize()} Level"
        )

        # ---------------------------------
        # QUESTIONS
        # ---------------------------------

        answers = []

        for i, q in enumerate(questions):

            st.markdown(
                f"### Q{i+1}. {q['question']}"
            )

            selected = st.radio(
                "Choose answer",
                q["options"],
                key=f"{subject}_{chapter}_{level}_{i}"
            )

            answers.append(
                (selected, q["answer"])
            )

        # ---------------------------------
        # SUBMIT QUIZ
        # ---------------------------------

        if st.button(
            f"Submit {level.capitalize()} Quiz",
            key=f"{subject}_{chapter}_{level}_submit"
        ):

            correct = 0

            for selected, actual in answers:

                if selected == actual:
                    correct += 1

            total = len(questions)

            percentage = round(
                (correct / total) * 100,
                2
            )

            st.success(
                f"Score: {correct}/{total}"
            )

            st.info(
                f"Accuracy: {percentage}%"
            )

            # ---------------------------------
            # SAVE MCQ ANALYTICS
            # ---------------------------------

            record_mcq_attempt(
                user=user,
                subject=selected_subject,
                chapter=selected_chapter,
                topic=topic,
                level=selected_level,
                correct=correct_answers,
                total=total_questions
            )

            # ---------------------------------
            # UNLOCK LOGIC
            # ---------------------------------

            if percentage >= 80:

                st.success(
                    f"🎉 {level.capitalize()} Completed!"
                )

                progress[level] = True

                st.session_state[
                    progress_key
                ] = progress

                if level == "basic":

                    st.success(
                        "🔓 Moderate Level Unlocked!"
                    )

                elif level == "moderate":

                    st.success(
                        "🔓 Advanced Level Unlocked!"
                    )

                elif level == "advanced":

                    st.balloons()

                    st.success(
                        "🏆 Chapter MCQs Fully Completed!"
                    )

            else:

                st.warning(
                    "Minimum 80% required to unlock next level."
                )

            st.rerun()

# =========================================================
# MAIN UI
# =========================================================
def core_subjects_ui(user):

    init_state()

    st.title("📚 Core Subjects")

    DATA = load_subjects()

    if not DATA:
        st.error("No data found")
        return

    subject = st.selectbox("📘 Select Subject", list(DATA.keys()))
    category = st.selectbox("📂 Select Category", list(DATA[subject].keys()))
    chapter = st.selectbox("📖 Select Chapter", list(DATA[subject][category].keys()))

    chapter_data = DATA[subject][category][chapter]

    topics = chapter_data.get("topics", [])

    if not topics:
        st.warning("No topics found")
        return

    if "topic_index" not in st.session_state:
        st.session_state.topic_index = 0

    idx = st.session_state.topic_index
    topic = topics[idx]

    st.markdown(f"## 📘 {topic.get('name')}")

    # =========================
    # ⭐ BOOKMARK (RESTORED)
    # =========================
    if st.button("⭐ Bookmark This Topic"):

        ok = add_bookmark(
            user,
            subject,
            category,
            chapter,
            topic.get("name"),
            idx
        )

        if ok:
            st.success("Bookmarked!")
        else:
            st.warning("Already bookmarked")

    # =========================
    # NOTES
    # =========================

    for note in topic.get("notes", []):

        st.markdown(f"### 🔹 {note.get('heading')}")

        for p in note.get("points", []):

            st.write("•", p)


    # =========================
    # MCQs (LOCKED SYSTEM)
    # =========================

    render_mcqs(
        user=user,
        subject=subject,
        chapter=chapter,
        mcqs=topic.get("mcqs", {})
    )


    # =========================
    # NAVIGATION
    # =========================

    col1, col2 = st.columns(2)