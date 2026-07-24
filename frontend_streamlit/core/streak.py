import streamlit as st
from core.leaderboard import get_leaderboard


def leaderboard_ui():

    st.header("🏆 Leaderboard")

    data = get_leaderboard()

    if not data:
        st.write("No scores yet")
        return

    for i, (user, score) in enumerate(data, 1):
        st.write(f"{i}. {user} — {score}")