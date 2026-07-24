import streamlit as st
from data.reasoning_data import reasoning_data


def reasoning_ui(user):

    st.title("🧩 Reasoning Practice")

    topic = st.selectbox("Select Topic", list(reasoning_data.keys()))

    questions = reasoning_data[topic]

    for i, q in enumerate(questions):
        st.write(f"Q{i+1}. {q['question']}")

        choice = st.radio("Answer", q["options"], key=f"r_{i}")

        if st.button(f"Check {i}", key=f"btn_r{i}"):
            if choice == q["answer"]:
                st.success("Correct ✅")
            else:
                st.error("Wrong ❌")