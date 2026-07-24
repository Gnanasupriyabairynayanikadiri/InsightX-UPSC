# ==============================
# 📁 FILE: core/leaderboard_ui.py
# FIXED + PRODUCTION STABLE VERSION
# ==============================

import streamlit as st

from core.xp import (
    get_leaderboard,
    get_rank,
    get_user_stats,
    get_level
)


# ==============================
# 🛡 SAFE NORMALIZER (CRITICAL FIX)
# ==============================
def normalize_leaderboard(data):

    formatted = []

    # ------------------------------
    # CASE 1: DICT FORMAT
    # ------------------------------
    if isinstance(data, dict):

        for user, value in data.items():

            if isinstance(value, dict):

                formatted.append({
                    "user": user,
                    "xp": value.get("xp", 0),
                    "streak": value.get("streak", 0)
                })

            else:

                formatted.append({
                    "user": user,
                    "xp": value,
                    "streak": 0
                })

    # ------------------------------
    # CASE 2: LIST FORMAT (EXPECTED)
    # ------------------------------
    elif isinstance(data, list):

        for item in data:

            if not item:
                continue

            if isinstance(item, dict):

                formatted.append({
                    "user": item.get("user") or item.get("username") or "unknown",
                    "xp": item.get("xp", 0),
                    "streak": item.get("streak", 0)
                })

            elif isinstance(item, (tuple, list)) and len(item) >= 2:

                user = item[0]
                stats = item[1]

                formatted.append({
                    "user": user,
                    "xp": stats.get("xp", 0) if isinstance(stats, dict) else stats,
                    "streak": stats.get("streak", 0) if isinstance(stats, dict) else 0
                })

    # ------------------------------
    # SORT SAFELY
    # ------------------------------
    formatted.sort(key=lambda x: x.get("xp", 0), reverse=True)

    return formatted


# ==============================
# 🏆 LEADERBOARD UI
# ==============================
def leaderboard_ui(username):

    st.title("🏆 UPSC Leaderboard")

    leaderboard = get_leaderboard()

    # ------------------------------
    # EMPTY STATE
    # ------------------------------
    if not leaderboard:
        st.info("No users on leaderboard yet.")
        return

    leaderboard = normalize_leaderboard(leaderboard)

    # ------------------------------
    # SAFE USER STATS
    # ------------------------------
    stats = get_user_stats(username) or {}

    xp = stats.get("xp", 0)
    streak = stats.get("streak", 0)
    level = get_level(xp)
    rank = get_rank(username)

    st.markdown("## 👤 Your Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⭐ XP", xp)
    c2.metric("🏅 Level", level)
    c3.metric("🔥 Streak", streak)
    c4.metric("🏆 Rank", rank)

    st.markdown("---")

    # ------------------------------
    # TOP 3
    # ------------------------------
    st.markdown("## 🥇 Top Performers")

    top_users = leaderboard[:3]
    medals = ["🥇", "🥈", "🥉"]

    cols = st.columns(3)

    for i, item in enumerate(top_users):

        with cols[i]:

            st.markdown(
                f"""
                <div style="
                    background:#1E1E2E;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                ">
                    <h2>{medals[i]}</h2>
                    <h3>{item.get('user', 'unknown')}</h3>
                    <p>⭐ {item.get('xp', 0)} XP</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ------------------------------
    # FULL LEADERBOARD
    # ------------------------------
    st.markdown("## 📊 Global Rankings")

    for index, item in enumerate(leaderboard, start=1):

        user = item.get("user", "unknown")
        user_xp = item.get("xp", 0)
        user_streak = item.get("streak", 0)
        level = get_level(user_xp)

        if user == username:

            st.success(
                f"""
🏆 Rank #{index}

👤 {user}

⭐ XP: {user_xp}

🏅 Level: {level}

🔥 Streak: {user_streak}
"""
            )

        else:

            st.markdown(
                f"""
                <div style="
                    background:#262730;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    <b>#{index} — {user}</b><br>
                    ⭐ XP: {user_xp} |
                    🏅 Level: {level} |
                    🔥 Streak: {user_streak}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ------------------------------
    # REFRESH BUTTON
    # ------------------------------
    st.markdown("---")

    if st.button("🔄 Refresh Leaderboard"):
        st.rerun()