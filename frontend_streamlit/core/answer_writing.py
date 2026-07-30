# =========================================================
# 📁 FILE: core/generator.py
# FULL FIXED + STABLE VERSION
# =========================================================

import random
import time
import streamlit as st


# =========================================================
# SAFE QUESTION BANK IMPORT
# =========================================================
try:

    from core.mains_engine.question_bank.question_bank_loader import QUESTION_BANK

except Exception:

    QUESTION_BANK = {

        "Polity": {

            "GS2": {

                "Parliament": {

                    "Basic": [

                        {
                            "question":
                            "Discuss the role of Parliament in Indian democracy.",

                            "marks": 10
                        },

                        {
                            "question":
                            "Explain the importance of Question Hour.",

                            "marks": 10
                        }
                    ],

                    "Moderate": [

                        {
                            "question":
                            "Analyze declining productivity of Parliament.",

                            "marks": 15
                        }
                    ],

                    "Advanced": [

                        {
                            "question":
                            "Critically evaluate Parliamentary Committees.",

                            "marks": 20
                        }
                    ]
                }
            }
        }
    }


# =========================================================
# CORE IMPORTS
# =========================================================
from core.question_analyzer import analyze_question

from core.answer_engine.evaluator import evaluate_answer

from core.answer_engine.generator import (
    generate_model_answer,
    generate_feedback,
    improve_answer
)

from core.plagiarism_checker import check_plagiarism

from core.xp import (

    reward_xp,
    get_xp,
    get_level
)

from core.answer_analytics import (
    record_answer_attempt,
    get_answer_stats
)

# =========================================================
# INIT SESSION
# =========================================================
def init_session():

    defaults = {

        "basic_full_scores": 0,

        "moderate_full_scores": 0,

        "current_question": None,

        "start_time": time.time(),

        "timer_running": False,

        "writing_started": False,

        "answer_box": ""
    }

    for k, v in defaults.items():

        if k not in st.session_state:

            st.session_state[k] = v


# =========================================================
# LEVEL UNLOCK SYSTEM
# =========================================================
def get_unlocked_levels():

    unlocked = ["Basic"]

    if st.session_state.get(

        "basic_full_scores",
        0

    ) >= 3:

        unlocked.append("Moderate")

    if st.session_state.get(

        "moderate_full_scores",
        0

    ) >= 3:

        unlocked.append("Advanced")

    return unlocked


# =========================================================
# TIMER
# =========================================================
def get_timer(level, marks):

    if level == "Basic":

        return 10 if marks == 10 else 15 if marks == 15 else 20

    if level == "Moderate":

        return 15 if marks == 10 else 20 if marks == 15 else 25

    if level == "Advanced":

        return 20 if marks == 10 else 25 if marks == 15 else 30

    return 10


# =========================================================
# RANDOM QUESTION
# =========================================================
def get_random_question(

    subject,
    category,
    chapter,
    level
):

    try:

        return random.choice(

            QUESTION_BANK[subject][category][chapter][level]
        )

    except Exception as e:

        st.error(

            f"Question loading failed: {e}"
        )

        return None


# =========================================================
# CLEAR RESULTS
# =========================================================
def clear_previous_results():

    keys = [

        "evaluation_result",

        "final_score",

        "feedback",

        "model_answer",

        "improved_answer",

        "plagiarism_result"
    ]

    for k in keys:

        st.session_state.pop(k, None)


# =========================================================
# QUESTION ANALYSIS UI
# =========================================================
def show_analysis(analysis):

    st.markdown("## 🧠 Question Analysis")

    st.info(

        f"Type: {analysis.get('type', 'Static')}"
    )

    st.info(

        f"Directive: {analysis.get('directive', 'Discuss')}"
    )

    st.info(

        f"Difficulty: {analysis.get('difficulty', 'Basic')}"
    )

    st.markdown("### 🔑 Keywords")

    st.success(

        ", ".join(
            analysis.get("keywords", [])
        )
    )

    st.markdown("### 🏗️ Structure")

    for p in analysis.get("structure", []):

        st.write(f"• {p}")


# =========================================================
# MAIN UI
# =========================================================
def answer_writing_ui(user):

    init_session()

    st.title("✍️ UPSC Answer Writing AI")

    st.markdown("---")

    # =====================================================
    # EMPTY QUESTION BANK
    # =====================================================
    if not QUESTION_BANK:

        st.error("QUESTION_BANK empty")

        return

    # =====================================================
    # SUBJECT
    # =====================================================
   
    subject = st.selectbox(
        "📚 Subject",
        list(QUESTION_BANK.keys()),
        key="aw_subject"
    )

    # =====================================================
    # CATEGORY
    # =====================================================

    category = st.selectbox(
        "📂 Category",
        list(QUESTION_BANK[subject].keys()),
        key="aw_category"
    )

    # =====================================================
    # CHAPTER
    # =====================================================

    chapter = st.selectbox(
        "📖 Chapter",
        list(QUESTION_BANK[subject][category].keys()),
        key="aw_chapter"
    )

    # =====================================================
    # LEVELS
    # =====================================================

    unlocked_levels = get_unlocked_levels()

    all_levels = list(
        QUESTION_BANK[subject][category][chapter].keys()
    )

    levels = [

        lvl

        for lvl in all_levels

        if lvl in unlocked_levels
    ]

    # =====================================================
    # LEVEL
    # =====================================================

    level = st.selectbox(
        "🎯 Level",
        levels,
        key="aw_level"
    )

    # =====================================================
    # PROGRESS
    # =====================================================
    st.info(

        f"Basic Unlock Progress: "
        f"{st.session_state.basic_full_scores}/3"
    )

    st.info(

        f"Moderate Unlock Progress: "
        f"{st.session_state.moderate_full_scores}/3"
    )

    # =====================================================
    # NEXT QUESTION
    # =====================================================
    if st.button("🔄 Next Question"):

        st.session_state.current_question = get_random_question(

            subject,
            category,
            chapter,
            level
        )

        st.session_state.start_time = time.time()

        st.session_state.timer_running = False

        st.session_state.writing_started = False

        st.session_state.answer_box = ""

        clear_previous_results()

        st.rerun()

    # =====================================================
    # LOAD QUESTION
    # =====================================================
    if st.session_state.current_question is None:

        st.session_state.current_question = get_random_question(

            subject,
            category,
            chapter,
            level
        )

    q = st.session_state.current_question

    if not q:

        st.error("No question found")

        return

    question = q["question"]

    marks = q["marks"]

    # =====================================================
    # DISPLAY QUESTION
    # =====================================================
    st.warning(question)

    st.write(f"Marks: {marks}")

    # =====================================================
    # QUESTION ANALYSIS
    # =====================================================
    analysis = analyze_question(question)

    show_analysis(analysis)

    # =====================================================
    # START WRITING
    # =====================================================
    if not st.session_state.writing_started:

        if st.button("🚀 Start Writing"):

            st.session_state.writing_started = True

            st.session_state.start_time = time.time()

            st.session_state.timer_running = True

            st.rerun()

    # =====================================================
    # WRITING MODE
    # =====================================================
    if st.session_state.writing_started:

        total_seconds = get_timer(level, marks) * 60

        elapsed = int(

            time.time() -
            st.session_state.start_time
        )

        remaining = max(

            total_seconds - elapsed,
            0
        )

        if remaining == 0:

            st.error("⏰ Time Up!")

        st.markdown(

            f"## ⏳ {remaining//60:02d}:{remaining%60:02d}"
        )

        answer = st.text_area(

            "Write Answer",

            height=400,

            key="answer_box"
        )

        col1, col2 = st.columns(2)

        submit = col1.button("Submit")

        post = col2.button("Post")

        # =================================================
        # SUBMIT ANSWER
        # =================================================
        if submit:

            st.session_state.timer_running = False
            st.session_state.writing_started = False

            if len(answer.strip()) < 30:

                st.error("Write more content")

                return

            # =============================================
            # EVALUATION
            # =============================================
            result = evaluate_answer(question, answer)

            st.session_state.evaluation_result = True

            score = result.get(

                "score",
                0
            )

            from core.answer_analytics import record_answer_attempt
            
            record_answer_attempt(
                user=user,
                subject=subject,
                chapter=chapter,
                level=level,
                score=score,
                out_of=10
            )

            from core.answer_analytics import get_answer_stats

            stats = get_answer_stats(user)

            st.markdown("## 📊 Answer Writing Progress")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Answers Written",
                    stats["attempts"]
                )

            with c2:
                st.metric(
                    "Average Score",
                    stats["average_score"]
                )

            with c3:
                st.metric(
                    "Highest Score",
                    stats["highest_score"]
                )

            st.success("✅ Answer Recorded Successfully")
            rank = result.get(

                "rank",
                "Average"
            )

            st.success(

                f"Score: {score}/10"
            )

            st.info(rank)

            # =============================================
            # FEEDBACK
            # =============================================
            feedback = generate_feedback(

                answer,
                question
            )

            st.info(feedback)

            # =============================================
            # MODEL ANSWER
            # =============================================
            model = generate_model_answer(question)

            st.markdown("## 🧠 Model Answer")

            st.write(model)

            # =============================================
            # IMPROVED ANSWER
            # =============================================
            improved = improve_answer(

                answer,
                question
            )

            st.markdown("## 🚀 Improved Version")

            st.write(improved)

            # =============================================
            # PLAGIARISM
            # =============================================
            plag = check_plagiarism(

                question,
                answer
            )

            similarity = plag.get(

                "similarity",
                0
            )

            st.write(

                f"Similarity: {similarity}%"
            )

            # =============================================
            # XP
            # =============================================
            xp = score * 5

            if similarity > 60:

                xp = 0

                st.error(

                    "XP blocked due to plagiarism"
                )

            reward_xp(user, xp)

            st.success(f"+{xp} XP")

            st.info(

                f"Total XP: {get_xp(user)}"
            )

            st.info(

                f"Level: "
                f"{get_level(get_xp(user))}"
            )

        # =================================================
        # COMMUNITY POST
        # =================================================
        if post:

            st.success("Posted to community")

        # =================================================
        # AUTO REFRESH TIMER
        # =================================================
        if st.session_state.timer_running and not st.session_state.get("evaluation_result"):

            time.sleep(1)

            st.rerun()