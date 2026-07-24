import streamlit as st
import random

from data.ncert_quiz import ncert_quiz

from core.xp import add_xp


# ==============================
# ⚙️ CONFIG
# ==============================
XP_REWARD = 5


# ==============================
# 🧹 SAFE GET
# ==============================
def safe_get(data, key, default=None):

    if default is None:
        default = []

    try:
        return data.get(key, default)

    except Exception:
        return default


# ==============================
# 📦 LOAD REVISION DATA
# ==============================
def get_revision_notes(path):

    try:

        subject, cls, chapter = path

        data = (
            ncert_quiz
            .get(subject, {})
            .get(cls, {})
            .get(chapter, {})
        )

        if not isinstance(data, dict):
            return []

        return safe_get(data, "notes", [])

    except Exception:
        return []


# ==============================
# 🧠 GENERATE REVISION QUESTIONS
# ==============================
def generate_revision_questions(notes):

    revision_questions = []

    for topic in notes:

        heading = topic.get("heading", "")

        points = topic.get("points", [])

        if not points:
            continue

        # Random point
        point = random.choice(points)

        revision_questions.append({
            "heading": heading,
            "answer": point
        })

    return revision_questions


# ==============================
# 🚀 MAIN UI
# ==============================
def revision_ui(user):

    st.title("🔁 Revision Mode")

    # ==============================
    # 📌 CHECK CHAPTER
    # ==============================
    path = st.session_state.get(
        "selected_path"
    )

    if not path or len(path) != 3:

        st.warning(
            "👉 Please select chapter first"
        )

        return

    subject, cls, chapter = path

    # ==============================
    # 📖 HEADER
    # ==============================
    st.markdown(
        f"""
### 📘 {subject}
### 📗 {cls}
### 📄 {chapter}
"""
    )

    # ==============================
    # 📦 LOAD NOTES
    # ==============================
    notes = get_revision_notes(path)

    if not notes:

        st.warning(
            "⚠️ No revision notes available"
        )

        return

    # ==============================
    # 🧠 INIT SESSION
    # ==============================
    if "revision_questions" not in st.session_state:

        st.session_state.revision_questions = (
            generate_revision_questions(notes)
        )

    if "revision_submitted" not in st.session_state:

        st.session_state.revision_submitted = False

    questions = st.session_state.revision_questions

    # ==============================
    # 📊 PROGRESS
    # ==============================
    st.progress(1.0)

    st.info(
        f"🧠 Total Revision Questions: {len(questions)}"
    )

    st.markdown("---")

    # ==============================
    # ✍️ QUESTIONS
    # ==============================
    answers = {}

    for i, q in enumerate(questions):

        st.markdown(
            f"## Q{i+1}. {q['heading']}"
        )

        user_input = st.text_area(
            "Write what you remember",
            key=f"revision_answer_{i}",
            height=120
        )

        answers[i] = user_input

    # ==============================
    # 🚀 SUBMIT
    # ==============================
    if st.button("✅ Submit Revision"):

        if st.session_state.revision_submitted:
            return

        st.session_state.revision_submitted = True

        score = 0

        results = []

        # ==============================
        # 📊 EVALUATION
        # ==============================
        for i, q in enumerate(questions):

            correct_answer = (
                q["answer"]
                .strip()
                .lower()
            )

            user_answer = (
                answers.get(i, "")
                .strip()
                .lower()
            )

            matched = False

            # Keyword matching
            keywords = correct_answer.split()

            matched_words = 0

            for word in keywords:

                if word in user_answer:
                    matched_words += 1

            # 50% keyword match
            if keywords:

                ratio = (
                    matched_words /
                    len(keywords)
                )

                matched = ratio >= 0.5

            if matched:
                score += 1

            results.append({
                "question": q["heading"],
                "correct": q["answer"],
                "user": user_answer,
                "matched": matched
            })

        total = len(questions)

        percent = int((score / total) * 100)

        # ==============================
        # 🎯 RESULT
        # ==============================
        st.markdown("# 🎯 Revision Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.success(f"✅ Score: {score}")

        with c2:
            st.info(f"📚 Total: {total}")

        with c3:
            st.warning(f"📈 Accuracy: {percent}%")

        st.progress(percent / 100)

        # ==============================
        # ⭐ XP REWARD
        # ==============================
        xp = score * XP_REWARD

        add_xp(user, xp)

        st.success(
            f"⭐ XP Earned: {xp}"
        )

        # ==============================
        # 🔥 FEEDBACK
        # ==============================
        if percent >= 90:

            st.success(
                "🔥 Excellent Recall!"
            )

        elif percent >= 70:

            st.info(
                "👍 Strong revision!"
            )

        elif percent >= 50:

            st.warning(
                "📚 Revise once more."
            )

        else:

            st.error(
                "⚠️ Needs serious revision."
            )

        # ==============================
        # 📄 REVIEW
        # ==============================
        st.markdown("---")

        st.markdown("## 📄 Answer Review")

        for i, r in enumerate(results, 1):

            if r["matched"]:

                st.success(
                    f"Q{i}. ✅ Good Recall"
                )

            else:

                st.error(
                    f"""
Q{i}. ❌ Weak Recall

Expected:
{r['correct']}
"""
                )

    # ==============================
    # 🔄 RETRY
    # ==============================
    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        if st.button("🔄 Retry Revision"):

            clear_revision_state()

            st.rerun()

    # ==============================
    # 🧠 GO TO QUIZ
    # ==============================
    with c2:

        if st.button("➡️ Go to Quiz"):

            clear_revision_state()

            st.session_state.menu = "Quiz"

            st.rerun()


# ==============================
# 🧹 CLEAR SESSION
# ==============================
def clear_revision_state():

    keys = [
        "revision_questions",
        "revision_submitted"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]