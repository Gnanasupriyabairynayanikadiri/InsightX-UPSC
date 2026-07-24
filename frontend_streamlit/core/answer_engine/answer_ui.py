# =========================================================
# 📁 core/answer_ui.py (CLEAN WRAPPER VERSION)
# =========================================================

import streamlit as st
from core.answer_writing import answer_writing_ui


# =========================================================
# MAIN UI WRAPPER
# =========================================================
def answer_ui(user):
    

    try:
        answer_writing_ui(user)

    except Exception as e:
        st.error("⚠️ Answer Writing Module Error")
        st.exception(e)

        st.info(
            "Fix suggestion: Refresh session or click Next Question"
        )