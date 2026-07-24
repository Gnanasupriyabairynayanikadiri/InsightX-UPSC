import streamlit as st
from data.pyq_data import PYQ_DATA
from core.xp import reward_user


# =========================================================
# 🧠 INIT STATE SAFELY
# =========================================================
def init_state():
    if "pyq_started" not in st.session_state:
        st.session_state.pyq_started = False

    if "pyq_submitted" not in st.session_state:
        st.session_state.pyq_submitted = False

    if "pyq_score" not in st.session_state:
        st.session_state.pyq_score = 0


# =========================================================
# 📚 PYQ UI
# =========================================================
def pyq_ui(user):

    init_state()

    st.title("📚 UPSC PYQ Practice Engine")

    # ==============================
    # 🎯 FILTERS
    # ==============================
    subjects = sorted(set(q["subject"] for q in PYQ_DATA))
    years = sorted(set(q["year"] for q in PYQ_DATA), reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        selected_subject = st.selectbox("Select Subject", ["All"] + subjects)

    with col2:
        selected_year = st.selectbox("Select Year", ["All"] + years)

    # ==============================
    # 🔍 FILTER LOGIC
    # ==============================
    filtered = PYQ_DATA

    if selected_subject != "All":
        filtered = [q for q in filtered if q["subject"] == selected_subject]

    if selected_year != "All":
        filtered = [q for q in filtered if q["year"] == selected_year]

    if not filtered:
        st.warning("No questions found")
        return

    # ==============================
    # ▶ START QUIZ
    # ==============================
    if st.button("🚀 Start PYQ Quiz"):
        st.session_state.pyq_started = True
        st.session_state.pyq_submitted = False
        st.session_state.pyq_score = 0

    # ==============================
    # 🧠 QUIZ FLOW
    # ==============================
    if st.session_state.pyq_started and not st.session_state.pyq_submitted:

        for i, q in enumerate(filtered):

            st.markdown(f"""
            <div style='background:#1E1E2F;padding:12px;border-radius:10px;margin-bottom:10px;'>
            📅 {q['year']} | 📚 {q['subject']} | 📌 {q['topic']}
            </div>
            """, unsafe_allow_html=True)

            st.write(f"Q{i+1}. {q['question']}")

            choice = st.radio(
                "Select answer",
                q["options"],
                key=f"pyq_{selected_subject}_{selected_year}_{i}"
            )

            st.session_state[f"ans_{i}"] = choice

    # ==============================
    # 📊 SUBMIT
    # ==============================
    if st.session_state.pyq_started and not st.session_state.pyq_submitted:

        if st.button("📊 Submit PYQ Quiz"):

            score = 0

            st.markdown("## 📊 Results")

            for i, q in enumerate(filtered):

                user_ans = st.session_state.get(f"ans_{i}")

                if user_ans == q["answer"]:
                    score += 1
                    st.success(f"Q{i+1} ✅ Correct")
                else:
                    st.error(f"Q{i+1} ❌ Wrong")
                    st.info(f"Correct Answer: {q['answer']}")

                st.write(f"💡 {q['explanation']}")
                st.markdown("---")

            # ==============================
            # 🏆 SCORE + XP
            # ==============================
            st.success(f"🎯 Final Score: {score} / {len(filtered)}")

            xp = score * 2
            reward_user(user, xp)

            st.info(f"⭐ You earned {xp} XP")

            st.session_state.pyq_score = score
            st.session_state.pyq_submitted = True

    # ==============================
    # 🔁 RESET BUTTON
    # ==============================
    if st.session_state.pyq_submitted:

        if st.button("🔁 Try Again"):
            st.session_state.pyq_started = False
            st.session_state.pyq_submitted = False
            st.session_state.pyq_score = 0
            st.rerun()