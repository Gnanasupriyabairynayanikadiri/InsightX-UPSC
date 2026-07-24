# =========================================================
# FILE: app/services/duplicate_detector.py
# SEMANTIC DUPLICATE DETECTOR
# =========================================================

from difflib import SequenceMatcher

print("DUPLICATE_DETECTOR LOADED")


def similarity(a: str, b: str):

    return SequenceMatcher(

        None,

        a.lower(),

        b.lower()

    ).ratio()


def is_duplicate(title, existing_titles, threshold=0.82):

    """
    Returns True if a similar title already exists.
    """

    for old_title in existing_titles:

        score = similarity(title, old_title)

        if score >= threshold:

            return True, old_title, score

    return False, None, 0