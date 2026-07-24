# ==========================================
# 📁 FILE: core/bookmarks_ui.py
# FIXED VERSION (USING FILE STORAGE ONLY)
# ==========================================

import streamlit as st

from core.bookmark_engine import (
    get_user_bookmarks,
    remove_bookmark
)


# ==========================================
# OPEN BOOKMARK (TEMP FUNCTION)
# ==========================================
def open_bookmark_local(bookmark):
    st.session_state["active_bookmark"] = bookmark
    st.success("Bookmark opened")


# ==========================================
# BOOKMARK UI
# ==========================================
def bookmarks_ui(user):

    st.title("⭐ Saved Bookmarks")

    # LOAD FROM FILE SYSTEM
    bookmarks = get_user_bookmarks(user)

    # ==========================================
    # EMPTY STATE
    # ==========================================
    if not bookmarks:
        st.info("No bookmarks saved yet")
        return

    # ==========================================
    # GROUP BY SUBJECT
    # ==========================================
    grouped = {}

    for b in bookmarks:
        subject = b.get("subject", "Unknown")

        if subject not in grouped:
            grouped[subject] = []

        grouped[subject].append(b)

    # ==========================================
    # DISPLAY
    # ==========================================
    for subject, items in grouped.items():

        st.markdown(f"## 📘 {subject}")

        for idx, b in enumerate(items):

            st.markdown(f"""
### 📂 {b.get('category', 'General')}
📖 Chapter: {b.get('chapter', '')}

🧠 Topic:
**{b.get('topic', '')}**
""")

            col1, col2 = st.columns(2)

            # OPEN
            with col1:
                if st.button(f"📖 Open", key=f"open_{subject}_{idx}"):

                    open_bookmark_local(b)
                    st.rerun()

            # REMOVE
            with col2:
                if st.button(f"🗑 Remove", key=f"rm_{subject}_{idx}"):

                    remove_bookmark(
                        user,
                        b.get("subject"),
                        b.get("chapter"),
                        b.get("topic")
                    )

                    st.success("Removed")
                    st.rerun()

            st.markdown("---")