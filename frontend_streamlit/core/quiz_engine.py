# =========================================================
# 📁 FILE: core/quiz_engine.py
# FINAL UPSC QUIZ ENGINE (LIVE TIMER + NCERT FIX)
# =========================================================

import streamlit as st
import random
import time

from data.ncert_quiz import ncert_quiz

from core.progress import (
    is_completed
)

from core.xp import (
    add_xp,
    ensure_user,
    get_xp,
    get_level
)


# =========================================================
# RESET QUIZ
# =========================================================
def reset_quiz():

    keys = [

        "quiz_started",
        "quiz_questions",
        "quiz_index",
        "quiz_score",
        "quiz_answers",
        "quiz_start_time",
        "quiz_completed"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]


# =========================================================
# LOAD QUIZ BANK
# =========================================================
def load_quiz_bank():

    try:

        return ncert_quiz

    except Exception:

        return {}


# =========================================================
# TIMER
# =========================================================
def get_timer():

    # 30 Minutes
    return 30 * 60


# =========================================================
# SAFE CHAPTER EXTRACTOR
# =========================================================
def get_chapters(class_data):

    chapters = {}

    # -----------------------------------------------------
    # CASE 1 → chapters key exists
    # -----------------------------------------------------
    if "chapters" in class_data:

        return class_data["chapters"]

    # -----------------------------------------------------
    # CASE 2 → direct structure
    # -----------------------------------------------------
    for key, value in class_data.items():

        if isinstance(value, dict):

            chapters[key] = value

    return chapters


# =========================================================
# EXTRACT MCQS
# =========================================================
def extract_mcqs(chapter):

    mcqs = []

    # -----------------------------------------------------
    # CASE 1 → mcqs key
    # -----------------------------------------------------
    if "mcqs" in chapter:

        mcq_data = chapter["mcqs"]

        # LIST
        if isinstance(mcq_data, list):

            mcqs.extend(mcq_data)

        # DICT LEVELS
        elif isinstance(mcq_data, dict):

            for _, value in mcq_data.items():

                if isinstance(value, list):

                    mcqs.extend(value)

    # -----------------------------------------------------
    # CASE 2 → quiz key
    # -----------------------------------------------------
    elif "quiz" in chapter:

        quiz_data = chapter["quiz"]

        if isinstance(quiz_data, list):

            mcqs.extend(quiz_data)

    # -----------------------------------------------------
    # CASE 3 → quizzes key
    # -----------------------------------------------------
    elif "quizzes" in chapter:

        quiz_data = chapter["quizzes"]

        if isinstance(quiz_data, list):

            mcqs.extend(quiz_data)

        elif isinstance(quiz_data, dict):

            for _, value in quiz_data.items():

                if isinstance(value, list):

                    mcqs.extend(value)

    # -----------------------------------------------------
    # CASE 4 → questions key
    # -----------------------------------------------------
    elif "questions" in chapter:

        question_data = chapter["questions"]

        if isinstance(question_data, list):

            mcqs.extend(question_data)

    return mcqs


# =========================================================
# MAIN QUIZ UI
# =========================================================
def quiz_ui(user):

    ensure_user(user)

    st.title("🧠 Quiz")

    QUIZ_BANK = load_quiz_bank()

    if not QUIZ_BANK:

        st.error("Quiz data not found")
        return

    # =====================================================
    # SUBJECT
    # =====================================================
    subjects = list(QUIZ_BANK.keys())

    subject = st.selectbox(

        "📚 Select Subject",

        subjects
    )

    subject_data = QUIZ_BANK.get(
        subject,
        {}
    )

    if not subject_data:

        st.warning("No subject data found")
        return

    # =====================================================
    # CLASS
    # =====================================================
    classes = list(subject_data.keys())

    selected_class = st.selectbox(

        "🏫 Select Class",

        classes
    )

    class_data = subject_data.get(
        selected_class,
        {}
    )

    if not class_data:

        st.warning("No class data found")
        return

    # =====================================================
    # CHAPTERS
    # =====================================================
    chapters = get_chapters(class_data)

    if not chapters:

        st.warning("No chapters found")
        return

    chapter_keys = list(chapters.keys())

    chapter_display_map = {

        f"{key} - {chapters[key].get('title', key)}": key

        for key in chapter_keys
    }

    selected_display = st.selectbox(

        "📖 Select Chapter",

        list(chapter_display_map.keys())
    )

    chapter_key = chapter_display_map[selected_display]

    chapter = chapters[chapter_key]

    # =====================================================
    # LOCK SYSTEM
    # =====================================================
    if not is_completed(
        user,
        subject,
        selected_class,
        chapter_key
    ):

        st.warning(
            "🔒 Complete this chapter in Learning section first."
        )

        st.stop()

    # =====================================================
    # QUESTIONS
    # =====================================================
    questions = extract_mcqs(chapter)

    if not questions:

        st.warning("No quiz questions available")

        st.info(
            "⚠️ MCQs not found inside this chapter structure."
        )

        st.write(chapter)

        return

    # =====================================================
    # START QUIZ
    # =====================================================
    if not st.session_state.get(
        "quiz_started",
        False
    ):

        st.info(

            f"""
📘 Subject: {subject}

🏫 Class: {selected_class}

📖 Chapter: {chapter.get('title', chapter_key)}

⏳ Timer: 30 Minutes
"""
        )

        if st.button("🚀 Start Quiz"):

            st.session_state.quiz_started = True

            st.session_state.quiz_questions = random.sample(

                questions,

                min(len(questions), 50)
            )

            st.session_state.quiz_index = 0

            st.session_state.quiz_score = 0

            st.session_state.quiz_answers = []

            st.session_state.quiz_start_time = time.time()

            st.session_state.quiz_completed = False

            st.rerun()

        return

    # =====================================================
    # LIVE TIMER
    # =====================================================
    total_seconds = get_timer()

    elapsed = int(

        time.time()

        -

        st.session_state.quiz_start_time
    )

    remaining = max(

        total_seconds - elapsed,
        0
    )

    if remaining == 0:

        st.error("⏰ Time Up!")

        st.session_state.quiz_completed = True

        st.rerun()

    st.markdown(

        f"## ⏳ {remaining//60:02d}:{remaining%60:02d}"
    )

    # =====================================================
    # QUIZ COMPLETED
    # =====================================================
    if st.session_state.get(
        "quiz_completed",
        False
    ):

        score = st.session_state.quiz_score

        total = len(

            st.session_state.quiz_questions
        )

        percentage = round(

            (score / total) * 100,
            2
        )

        st.success(

            f"🏆 Final Score: {score}/{total}"
        )

        st.info(

            f"📊 Percentage: {percentage}%"
        )

        # =================================================
        # XP
        # =================================================
        xp_earned = score * 5

        add_xp(
            user,
            xp_earned
        )
        from core.quiz_analytics import save_quiz_attempt

        save_quiz_attempt(
            user=user,
            subject=subject,
            chapter=chapter_key,
            score=score,
            total=total
        )
        st.success(
            f"⭐ XP Earned: +{xp_earned}"
        )

        st.markdown("---")

        # =================================================
        # REVIEW
        # =================================================
        st.markdown("## 📘 Quiz Review")

        for idx, item in enumerate(

            st.session_state.quiz_answers,
            start=1
        ):

            st.markdown(

                f"### Q{idx}. {item['question']}"
            )

            st.write(

                f"✅ Correct Answer: {item['correct']}"
            )

            st.write(

                f"📝 Your Answer: {item['selected']}"
            )

            if item["is_correct"]:

                st.success("Correct")

            else:

                st.error("Wrong")

            st.markdown("---")

        # =================================================
        # RETAKE
        # =================================================
        if st.button("🔄 Retake Quiz"):

            reset_quiz()

            st.rerun()

        return

    # =====================================================
    # CURRENT QUESTION
    # =====================================================
    index = st.session_state.quiz_index

    current = st.session_state.quiz_questions[
        index
    ]

    question = current.get(
        "question",
        "Question missing"
    )

    options = current.get(
        "options",
        []
    )

    answer = current.get(
        "answer",
        ""
    )

    st.markdown(

        f"## Question {index + 1}"
    )

    st.info(question)

    # =====================================================
    # OPTIONS
    # =====================================================
    selected = st.radio(

        "Choose Answer",

        options,

        key=f"quiz_{index}"
    )

    # =====================================================
    # NEXT
    # =====================================================
    if st.button("➡️ Next"):

        is_correct = selected == answer

        if is_correct:

            st.session_state.quiz_score += 1

        st.session_state.quiz_answers.append({

            "question": question,

            "selected": selected,

            "correct": answer,

            "is_correct": is_correct
        })

        # =================================================
        # NEXT QUESTION
        # =================================================
        if index + 1 >= len(

            st.session_state.quiz_questions
        ):

            st.session_state.quiz_completed = True

        else:

            st.session_state.quiz_index += 1

        st.rerun()

    # =====================================================
    # SIDEBAR
    # =====================================================
    with st.sidebar:

        st.markdown("## 📊 Quiz Stats")

        st.write(

            f"👤 User: {user}"
        )

        st.write(

            f"⭐ XP: {get_xp(user)}"
        )

        st.write(

            f"🏅 Level: {get_level(user)}"
        )

        st.write(

            f"✅ Score: {st.session_state.quiz_score}"
        )

        st.write(

            f"❓ Question: {index + 1}/{len(st.session_state.quiz_questions)}"
        )

        st.markdown("---")

        if st.button("❌ Exit Quiz"):

            reset_quiz()

            st.rerun()

    # =====================================================
    # LIVE REFRESH
    # =====================================================
    time.sleep(1)

    st.rerun()