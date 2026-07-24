import streamlit as st

from data.csat_data import csat_data

from core.progress import (
    mark_level_completed,
    is_level_completed,
    get_level_progress
)

from core.xp import reward_user


# =========================================================
# 📌 SESSION INIT
# =========================================================
def init_session():

    defaults = {

        "csat_subject": None,

        "csat_topic": None,

        "csat_level": "basic",

        "csat_answers": {},

        "csat_bookmarks": [],

        "csat_resume": {}
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =========================================================
# 📌 SAVE RESUME
# =========================================================
def save_resume(subject, topic):

    st.session_state.csat_resume = {

        "subject": subject,

        "topic": topic
    }


# =========================================================
# 📌 MAIN UI
# =========================================================
def csat_ui(user):

    init_session()

    st.title("🧠 CSAT Practice")

    # =====================================================
    # SUBJECT SELECT
    # =====================================================
    if not st.session_state.csat_subject:

        st.subheader("📘 Select CSAT Section")

        subjects = sorted(csat_data.keys())

        cols = st.columns(2)

        for i, subject in enumerate(subjects):

            with cols[i % 2]:

                if st.button(
                    subject,
                    use_container_width=True
                ):

                    st.session_state.csat_subject = subject

                    st.rerun()

        return

    # =====================================================
    # CURRENT SUBJECT
    # =====================================================
    subject = st.session_state.csat_subject

    # =====================================================
    # TOPIC SELECT
    # =====================================================
    if not st.session_state.csat_topic:

        st.subheader(f"📂 {subject}")

        topics = sorted(
            csat_data[subject].keys()
        )

        for topic in topics:

            col1, col2 = st.columns([5, 1])

            with col1:

                if st.button(
                    topic,
                    key=f"topic_{topic}",
                    use_container_width=True
                ):

                    st.session_state.csat_topic = topic

                    st.rerun()

            with col2:

                if st.button(
                    "⭐",
                    key=f"bookmark_{topic}"
                ):

                    bookmark = {

                        "subject": subject,

                        "topic": topic
                    }

                    if (
                        bookmark
                        not in st.session_state.csat_bookmarks
                    ):

                        st.session_state.csat_bookmarks.append(
                            bookmark
                        )

                        st.success(
                            "Bookmarked!"
                        )

        st.markdown("---")

        # =================================================
        # RESUME
        # =================================================
        if st.session_state.csat_resume:

            resume = st.session_state.csat_resume

            st.markdown("### 🔁 Resume Study")

            st.write(
                f"📘 {resume['subject']}"
            )

            st.write(
                f"📖 {resume['topic']}"
            )

            if st.button(
                "Continue Learning"
            ):

                st.session_state.csat_subject = (
                    resume["subject"]
                )

                st.session_state.csat_topic = (
                    resume["topic"]
                )

                st.rerun()

        # =================================================
        # BOOKMARKS
        # =================================================
        if st.session_state.csat_bookmarks:

            st.markdown("### ⭐ Bookmarks")

            for i, b in enumerate(
                st.session_state.csat_bookmarks
            ):

                label = (
                    f"{b['subject']} → "
                    f"{b['topic']}"
                )

                if st.button(
                    label,
                    key=f"bkm_{i}"
                ):

                    st.session_state.csat_subject = (
                        b["subject"]
                    )

                    st.session_state.csat_topic = (
                        b["topic"]
                    )

                    st.rerun()

        st.markdown("---")

        if st.button("⬅ Back to Subjects"):

            st.session_state.csat_subject = None

            st.rerun()

        return

    # =====================================================
    # CURRENT TOPIC
    # =====================================================
    topic = st.session_state.csat_topic

    save_resume(subject, topic)

    st.subheader(
        f"📘 {subject} → {topic}"
    )

    # =====================================================
    # LEVEL UNLOCK SYSTEM
    # =====================================================
    levels = ["basic"]

    if is_level_completed(
        user,
        "CSAT",
        topic,
        "basic"
    ):

        levels.append("moderate")

    if is_level_completed(
        user,
        "CSAT",
        topic,
        "moderate"
    ):

        levels.append("advanced")

    # =====================================================
    # LEVEL SELECT
    # =====================================================
    level = st.selectbox(
        "🎯 Select Level",
        levels
    )

    st.session_state.csat_level = level

    # =====================================================
    # PROGRESS
    # =====================================================
    progress = get_level_progress(
        user,
        "CSAT",
        topic
    )

    st.markdown("## 📊 Progress")

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Basic",
        "✅" if progress["basic"] else "❌"
    )

    p2.metric(
        "Moderate",
        "✅" if progress["moderate"] else "❌"
    )

    p3.metric(
        "Advanced",
        "✅" if progress["advanced"] else "❌"
    )

    st.markdown("---")

    # =====================================================
    # QUESTIONS
    # =====================================================
    questions = (
        csat_data[subject][topic]
        .get(level, [])
    )

    if not questions:

        st.warning(
            "No questions available"
        )

        return

    st.subheader(
        f"🧠 {level.capitalize()} Questions"
    )

    # =====================================================
    # RENDER QUESTIONS
    # =====================================================
    for i, q in enumerate(questions):

        st.markdown(
            f"### Q{i+1}. {q.get('question', '')}"
        )

        # =================================================
        # PASSAGE
        # =================================================
        if "passage" in q:

            st.info(q["passage"])

        # =================================================
        # OPTIONS
        # =================================================
        key = (
            f"{subject}_"
            f"{topic}_"
            f"{level}_"
            f"{i}"
        )

        selected = st.radio(

            "Choose answer",

            q["options"],

            key=key
        )

        st.session_state.csat_answers[key] = selected

    # =====================================================
    # SUBMIT QUIZ
    # =====================================================
    if st.button("✅ Submit Quiz"):

        score = 0

        for i, q in enumerate(questions):

            key = (
                f"{subject}_"
                f"{topic}_"
                f"{level}_"
                f"{i}"
            )

            selected = (
                st.session_state
                .csat_answers
                .get(key)
            )

            if selected == q["answer"]:

                score += 1

        total = len(questions)

        st.success(
            f"🎯 Score: {score}/{total}"
        )

        # =================================================
        # REVIEW ANSWERS
        # =================================================
        st.markdown("## 📖 Answer Review")

        for i, q in enumerate(questions):

            key = (
                f"{subject}_"
                f"{topic}_"
                f"{level}_"
                f"{i}"
            )

            selected = (
                st.session_state
                .csat_answers
                .get(key)
            )

            correct = q["answer"]

            if selected == correct:

                st.success(
                    f"Q{i+1}: Correct ✅"
                )

            else:

                st.error(
                    f"Q{i+1}: Wrong ❌"
                )

                st.info(
                    f"Correct Answer: {correct}"
                )

            # =============================================
            # EXPLANATION
            # =============================================
            if "explanation" in q:

                st.write(
                    f"🧠 Explanation: "
                    f"{q['explanation']}"
                )

        # =================================================
        # LEVEL COMPLETE
        # =================================================
        if score >= 3:

            mark_level_completed(
                user,
                "CSAT",
                topic,
                level
            )

            st.success(
                f"✅ {level.capitalize()} Level Completed!"
            )

            st.balloons()

        else:

            st.warning(
                "⚠️ Need at least 3 correct answers to unlock next level"
            )

        # =================================================
        # XP SYSTEM
        # =================================================
        xp = score * 2

        reward_user(user, xp)

        st.info(
            f"⭐ XP Earned: {xp}"
        )

        accuracy = int(
            (score / total) * 100
        )

        st.progress(
            accuracy / 100
        )

        st.write(
            f"📊 Accuracy: {accuracy}%"
        )

    st.markdown("---")

    # =====================================================
    # NAVIGATION
    # =====================================================
    c1, c2 = st.columns(2)

    with c1:

        if st.button("⬅ Back to Topics"):

            st.session_state.csat_topic = None

            st.rerun()

    with c2:

        if st.button("🏠 Back to Subjects"):

            st.session_state.csat_subject = None

            st.session_state.csat_topic = None

            st.rerun()