from datetime import datetime, date

from core.storage import (
    load_json,
    save_json
)

from core.utils import normalize


FILE = "storage/top_answer.json"


# ==============================
# LOAD DATA
# ==============================
def load_top_answers():

    return load_json(FILE, {})


# ==============================
# SAVE DATA
# ==============================
def save_top_answers(data):

    save_json(FILE, data)


# ==============================
# GET TODAY KEY
# ==============================
def get_today():

    return str(date.today())


# ==============================
# UPDATE TOP ANSWER
# ==============================
def update_top_answer(
    user,
    question,
    answer,
    score
):

    user = normalize(user)

    data = load_top_answers()

    today = get_today()

    # ==============================
    # INIT DAY
    # ==============================
    if today not in data:

        data[today] = {
            "top_answer": None,
            "history": []
        }

    # ==============================
    # STORE HISTORY
    # ==============================
    data[today]["history"].append({
        "user": user,
        "question": question,
        "score": score,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    current_top = data[today]["top_answer"]

    # ==============================
    # UPDATE TOP ANSWER
    # ==============================
    if (
        current_top is None or
        score > current_top["score"]
    ):

        data[today]["top_answer"] = {

            "user": user,

            "question": question,

            "answer": answer,

            "score": score,

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    save_top_answers(data)

    return True


# ==============================
# GET TODAY TOP ANSWER
# ==============================
def get_top_answer():

    data = load_top_answers()

    today = get_today()

    day_data = data.get(today, {})

    return day_data.get("top_answer")


# ==============================
# GET FULL HISTORY
# ==============================
def get_answer_history():

    data = load_top_answers()

    today = get_today()

    day_data = data.get(today, {})

    return day_data.get("history", [])


# ==============================
# GET TOP USER
# ==============================
def get_top_user():

    top = get_top_answer()

    if not top:
        return None

    return top.get("user")


# ==============================
# GET TOP SCORE
# ==============================
def get_top_score():

    top = get_top_answer()

    if not top:
        return 0

    return top.get("score", 0)