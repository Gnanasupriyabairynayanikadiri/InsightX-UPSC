# =========================================================
# 📁 FILE: core/daily_challenge.py
# =========================================================

import os
import json
import random

from datetime import (
    datetime,
    date
)

from core.answer_eval import (
    evaluate_answer
)

from core.xp import add_xp

from core.ai_model_answer import (
    generate_model_answer
)


# =========================================================
# STORAGE
# =========================================================
FILE = "storage/daily_challenge.json"

QUESTION_FILE = "storage/daily_question.json"


# =========================================================
# ENSURE STORAGE
# =========================================================
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

    if not os.path.exists(QUESTION_FILE):

        with open(

            QUESTION_FILE,
            "w",
            encoding="utf-8"

        ) as f:

            json.dump({}, f)


# =========================================================
# LOAD JSON
# =========================================================
def load_json(path):

    ensure_storage()

    try:

        with open(

            path,
            "r",
            encoding="utf-8"

        ) as f:

            return json.load(f)

    except:

        return {}


# =========================================================
# SAVE JSON
# =========================================================
def save_json(path, data):

    ensure_storage()

    with open(

        path,
        "w",
        encoding="utf-8"

    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# LOAD QUESTION BANK
# =========================================================
def load_question_bank():

    try:

        from core.mains_engine.question_bank.question_bank_loader import (
            load_question_bank
        )

        return load_question_bank()

    except:

        return {}


# =========================================================
# GET ALL QUESTIONS
# =========================================================
def get_all_questions():

    bank = load_question_bank()

    all_questions = []

    for subject, subject_data in bank.items():

        if not isinstance(subject_data, dict):
            continue

        for category, category_data in subject_data.items():

            if not isinstance(category_data, dict):
                continue

            # =================================================
            # DIRECT LEVEL FORMAT
            # =================================================
            if "Basic" in category_data:

                for level, questions in category_data.items():

                    for q in questions:

                        all_questions.append({

                            "subject": subject,

                            "category": None,

                            "chapter": category,

                            "level": level,

                            "question": q.get("question", ""),

                            "marks": q.get("marks", 10)
                        })

            # =================================================
            # CATEGORY → CHAPTER → LEVEL
            # =================================================
            else:

                for chapter, chapter_data in category_data.items():

                    if not isinstance(chapter_data, dict):
                        continue

                    for level, questions in chapter_data.items():

                        for q in questions:

                            all_questions.append({

                                "subject": subject,

                                "category": category,

                                "chapter": chapter,

                                "level": level,

                                "question": q.get("question", ""),

                                "marks": q.get("marks", 10)
                            })

    return all_questions


# =========================================================
# GENERATE DAILY QUESTION
# =========================================================
def generate_daily_question():

    all_questions = get_all_questions()

    if not all_questions:

        return None

    today = str(date.today())

    # =====================================================
    # FIXED RANDOM SEED
    # =====================================================
    random.seed(today)

    selected = random.choice(all_questions)

    return selected


# =========================================================
# GET DAILY QUESTION
# =========================================================
def get_daily_question():

    data = load_json(QUESTION_FILE)

    today = str(date.today())

    # =====================================================
    # EXISTING TODAY QUESTION
    # =====================================================
    if data.get("date") == today:

        return data.get("question")

    # =====================================================
    # NEW QUESTION
    # =====================================================
    question = generate_daily_question()

    data = {

        "date": today,

        "question": question
    }

    save_json(
        QUESTION_FILE,
        data
    )

    return question


# =========================================================
# LOAD DAILY DATA
# =========================================================
def load_daily_data():

    return load_json(FILE)


# =========================================================
# SAVE DAILY DATA
# =========================================================
def save_daily_data(data):

    save_json(FILE, data)


# =========================================================
# CHECK COMPLETED
# =========================================================
def daily_completed(user):

    data = load_daily_data()

    today = str(date.today())

    user_data = data.get(user, {})

    return today in user_data


# =========================================================
# DAILY XP BONUS
# =========================================================
def daily_xp_bonus(score):

    if score >= 9:
        return 50

    elif score >= 7:
        return 35

    elif score >= 5:
        return 20

    return 10


# =========================================================
# SUBMIT DAILY ANSWER
# =========================================================
def submit_daily_answer(

    user,
    answer

):

    question_data = get_daily_question()

    if not question_data:

        return {

            "success": False,

            "message": "No question available"
        }

    question = question_data["question"]

    # =====================================================
    # AI EVALUATION
    # =====================================================
    result = evaluate_answer(

        question,
        answer,
        use_ai=True
    )

    score = result.get(
        "score",
        0
    )

    bonus_xp = daily_xp_bonus(score)

    # =====================================================
    # SAVE DATA
    # =====================================================
    data = load_daily_data()

    today = str(date.today())

    if user not in data:

        data[user] = {}

    data[user][today] = {

        "question": question,

        "answer": answer,

        "score": score,

        "xp": bonus_xp,

        "date": str(datetime.now()),

        "evaluation": result
    }

    save_daily_data(data)

    # =====================================================
    # ADD XP
    # =====================================================
    add_xp(
        user,
        bonus_xp
    )

    # =====================================================
    # MODEL ANSWER
    # =====================================================
    model_answer = generate_model_answer(

        question,
        marks=question_data.get(
            "marks",
            10
        )
    )

    return {

        "success": True,

        "question": question,

        "score": score,

        "xp": bonus_xp,

        "evaluation": result,

        "model_answer": model_answer
    }


# =========================================================
# USER DAILY HISTORY
# =========================================================
def get_user_daily_history(user):

    data = load_daily_data()

    return data.get(user, {})


# =========================================================
# DAILY LEADERBOARD
# =========================================================
def daily_leaderboard():

    data = load_daily_data()

    today = str(date.today())

    board = []

    for user, user_data in data.items():

        if today in user_data:

            item = user_data[today]

            board.append({

                "user": user,

                "score": item.get(
                    "score",
                    0
                ),

                "xp": item.get(
                    "xp",
                    0
                )
            })

    board = sorted(

        board,

        key=lambda x: (

            x["score"],
            x["xp"]

        ),

        reverse=True
    )

    return board


# =========================================================
# DAILY STATS
# =========================================================
def daily_stats():

    leaderboard = daily_leaderboard()

    total_users = len(leaderboard)

    avg_score = 0

    if leaderboard:

        avg_score = round(

            sum(

                x["score"]

                for x in leaderboard

            )

            /

            len(leaderboard),

            2
        )

    return {

        "participants": total_users,

        "average_score": avg_score
    }


# =========================================================
# USER DAILY RANK
# =========================================================
def user_daily_rank(user):

    board = daily_leaderboard()

    for i, item in enumerate(board, start=1):

        if item["user"] == user:

            return i

    return None


# =========================================================
# DAILY CHALLENGE STATUS
# =========================================================
def daily_status(user):

    completed = daily_completed(user)

    rank = user_daily_rank(user)

    stats = daily_stats()

    return {

        "completed": completed,

        "rank": rank,

        "participants": stats["participants"],

        "average_score": stats["average_score"]
    }