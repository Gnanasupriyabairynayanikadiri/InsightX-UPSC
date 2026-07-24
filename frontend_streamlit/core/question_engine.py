from core.constants import QUESTION_BANK
import random


# =========================================================
# NORMALIZE KEYS (CRITICAL FIX)
# =========================================================
def norm(text):
    return str(text).strip()


# =========================================================
# GET QUESTIONS SAFE
# =========================================================
def get_questions(subject, category, chapter, level):

    try:
        bank = QUESTION_BANK

        return bank[subject][category][chapter][level]

    except KeyError:
        return []


# =========================================================
# GET RANDOM QUESTION
# =========================================================
def get_random_question(subject, category, chapter, level):

    questions = get_questions(subject, category, chapter, level)

    if not questions:
        return None

    return random.choice(questions)