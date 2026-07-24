# ==============================
# 📁 FILE: core/learning.py
# MOBILE READY + STABLE VERSION
# ==============================

import streamlit as st
import json
import os
from data.ncert_quiz import ncert_quiz
from core.progress import (
    mark_completed as progress_mark_completed,
    is_completed
)








# ==============================
# SAFE STRUCTURE CLEANER (IMPORTANT FIX)
# ==============================
def extract_chapters(class_data):
    """
    Handles messy or nested structures safely
    """

    # Case 1: proper structure
    if "chapters" in class_data:
        return class_data["chapters"]

    # Case 2: already chapter dict
    if any(isinstance(v, dict) and "title" in v for v in class_data.values()):
        return class_data

    return {}


def safe_title(key, data):
    if isinstance(data, dict):
        return data.get("title") or data.get("name") or str(key)
    return str(key)


# ==============================
# UI (CLEAN + MOBILE READY)
# ==============================
def learning_ui(user):

    st.title("📚 NCERT Learning")

    # ----------------------
    # SUBJECT
    # ----------------------
    subjects = list(ncert_quiz.keys())
    subject = st.selectbox("📘 Select Subject", subjects)

    # ----------------------
    # CLASS
    # ----------------------
    class_data_raw = ncert_quiz[subject]

    classes = list(class_data_raw.keys())
    class_name = st.selectbox("🏫 Select Class", classes)

    class_data = class_data_raw[class_name]

    # ----------------------
    # FIX: CHAPTER EXTRACTION
    # ----------------------
    chapters = extract_chapters(class_data)

    if not chapters:
        st.error("No chapters found in this class.")
        return

    # ----------------------
    # BUILD CLEAN OPTIONS
    # ----------------------
    options = []
    mapping = {}

    for key, value in chapters.items():
        title = safe_title(key, value)
        label = f"{title}"   # MOBILE CLEAN UI (no clutter)
        options.append(label)
        mapping[label] = key

    # ----------------------
    # SELECT CHAPTER
    # ----------------------
    selected = st.selectbox("📖 Select Chapter", options)

    chapter_key = mapping[selected]
    chapter = chapters.get(chapter_key, {})

    title = safe_title(chapter_key, chapter)

    st.header(title)

    # ----------------------
    # NOTES
    # ----------------------
    if isinstance(chapter, dict):

        notes = chapter.get("notes", [])

        if notes:
            st.subheader("📝 Notes")

            for section in notes:
                st.markdown(f"### {section.get('heading','')}")

                for point in section.get("points", []):
                    st.write("•", point)

        # ----------------------
        # QUICK REVISION BUTTON
        # ----------------------
        revision = chapter.get("revision", [])

        if revision:
            st.subheader("⚡ Quick Revision")

            if st.button("🔁 Show Revision"):
                for point in revision:
                    st.success(point)

    # ----------------------
    # COMPLETION
    # ----------------------
    if is_completed(
        user,
        subject,
        class_name,
        chapter_key
    ):

        st.success("✅ Chapter Completed")

    else:

        if st.button("Mark as Completed"):

            progress_mark_completed(
                user,
                subject,
                class_name,
                chapter_key
            )

            st.success("Saved!")

            st.rerun()