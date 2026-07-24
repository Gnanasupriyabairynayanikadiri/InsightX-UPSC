# core/csat.py

import streamlit as st

from data.csat_data import csat_data

from core.xp import add_xp
from core.progress import (
    mark_level_completed,
    is_level_completed
)

# ==============================
# SAFE GET
# ==============================
def safe_get(data, key, default=None):

    try:
        return data.get(key, default)
    except Exception:
        return default


# ==============================
# INIT SESSION
# ==============================
def init_session():

    defaults = {
        "csat_subject": None,
        "csat_topic": None,
        "csat_level": "basic",
        "csat_answers": {},
        "csat_score": 0,
        "csat_submitted": False
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# ==============================
# RESET QUIZ
# ==============================
def reset_quiz():

    st.session_state.csat_answers = {}
    st.session_state.csat_score = 0
    st.session_state.csat_submitted = False


# ==============================
# GET AVAILABLE LEVELS
# ==============================
def get_available_levels(user, subject, topic):

    levels = ["basic"]

    if is_level_completed(user, subject, topic, "basic"):
        levels.append("moderate")

    if is_level_completed(user, subject, topic, "moderate"):
        levels.append("advanced")

    return levels


# ==============================
# MAIN UI
# ==============================
def csat_ui(user):

    init_session()

    st.title("🧠 CSAT Practice")

    # ==============================
    # SUBJECT
    # ==============================
    subjects = list(csat_data.keys())

    if not subjects:
        st.error("No CSAT data found.")
        return

    subject = st.selectbox(
        "📘 Select Section",
        subjects
    )

    # ==============================
    # TOPIC
    # ==============================
    topics = list(csat_data[subject].keys())

    if not topics:
        st.warning("No topics found.")
        return

    topic = st.selectbox(
        "📂 Select Topic",
        topics
    )

    # ==============================
    # LEVEL
    # ==============================
    available_levels = get_available_levels(
        user,
        subject,
        topic
    )

    level = st.selectbox(
        "🎯 Select Level",
        available_levels
    )

    # ==============================
    # QUESTIONS
    # ==============================
    level_questions = safe_get(
        csat_data[subject][topic],
        level,
        []
    )

    if not level_questions:

        st.warning("No questions available.")
        return

    st.markdown("---")

    st.subheader(
        f"📚 {subject} → {topic} → {level.capitalize()}"
    )

    # ==============================
    # QUESTIONS UI
    # ==============================
    for i, q in enumerate(level_questions):

        st.markdown(f"### Q{i+1}. {q['question']}")

        # --------------------------
        # PASSAGE SUPPORT
        # --------------------------
        if "passage" in q:

            st.info(q["passage"])

        selected = st.radio(
            "Choose Answer",
            q["options"],
            key=f"{subject}_{topic}_{level}_{i}"
        )

        st.session_state.csat_answers[i] = selected

        st.markdown("---")

    # ==============================
    # SUBMIT QUIZ
    # ==============================
    if st.button("✅ Submit Quiz"):

        score = 0

        for i, q in enumerate(level_questions):

            selected = st.session_state.csat_answers.get(i)

            if selected == q["answer"]:
                score += 1

        st.session_state.csat_score = score
        st.session_state.csat_submitted = True

        # ==============================
        # RESULT
        # ==============================
        st.success(
            f"🎯 Score: {score} / {len(level_questions)}"
        )

        percent = int((score / len(level_questions)) * 100)

        st.info(f"📊 Accuracy: {percent}%")

        # ==============================
        # XP
        # ==============================
        xp = score * 5

        add_xp(user, xp)

        st.success(f"⭐ XP Earned: {xp}")

        # ==============================
        # LEVEL COMPLETE
        # ==============================
        if score >= 3:

            mark_level_completed(
                user,
                subject,
                topic,
                level
            )

            st.success(
                f"✅ {level.capitalize()} level unlocked!"
            )

            st.balloons()

        else:

            st.warning(
                "⚠️ Score at least 3 to unlock next level."
            )

        st.markdown("---")

        # ==============================
        # ANSWER REVIEW
        # ==============================
        st.subheader("📝 Answer Review")

        for i, q in enumerate(level_questions):

            selected = st.session_state.csat_answers.get(i)

            st.markdown(f"### Q{i+1}. {q['question']}")

            st.write(f"✅ Correct Answer: {q['answer']}")
            st.write(f"🖊️ Your Answer: {selected}")

            if selected == q["answer"]:
                st.success("Correct")
            else:
                st.error("Wrong")

            # Explanation
            if "explanation" in q:

                st.info(q["explanation"])

            st.markdown("---")

    # ==============================
    # RESET
    # ==============================
    if st.button("🔄 Reset Quiz"):

        reset_quiz()

        st.rerun()