# =========================================
# 📁 FILE: core/community_ui.py
# =========================================

import streamlit as st  
# Import Streamlit library to build UI (web app framework)

from core.community import (
    add_post,     # Function to add a new post to database/storage
    get_posts,    # Function to fetch posts (latest / most liked)
    render_post   # Function to display a single post UI
)


# =========================================
# MAIN COMMUNITY UI FUNCTION
# =========================================
def community_ui(user):
    # Main function that renders the entire community page
    # "user" is the currently logged-in user

    st.title("🌍 InsightX Community")
    # Page title shown at top of UI

    # =====================================
    # CREATE POST SECTION
    # =====================================
    st.markdown("## ✍️ Create Community Post")
    # Section heading

    content = st.text_area(
        "Share notes, doubts, strategy, motivation...",
        height=150,
        placeholder="""
Examples:

• UPSC strategy
• Notes
• Doubts
• Motivation
• Answer writing insights
• Current affairs analysis
"""
    )
    # Text input box where user writes post content

    image = st.file_uploader(
        "📷 Upload Image (Optional)",
        type=["png", "jpg", "jpeg"]
    )
    # Optional image upload for post

    # =====================================
    # POST BUTTON LOGIC
    # =====================================
    if st.button("🚀 Publish Post"):
        # Runs when user clicks Publish button

        if not content.strip() and not image:
            # If both text and image are empty

            st.warning("Write something or upload image")
            # Show warning message

        else:
            # If valid content exists

            add_post(
                user=user,
                content=content,
                image=image
            )
            # Save post to backend/storage

            st.success("✅ Posted successfully!")
            # Show success message

            st.rerun()
            # Refresh page to show new post

    st.markdown("---")
    # Horizontal separator line

    # =====================================
    # SORT OPTIONS SECTION
    # =====================================
    col1, col2 = st.columns([2, 1])
    # Split UI into two columns

    with col1:
        sort_by = st.selectbox(
            "📊 Sort Feed",
            [
                "Latest",
                "Most Liked"
            ]
        )
        # Dropdown to choose sorting method

    with col2:
        refresh = st.button("🔄 Refresh")
        # Button to manually refresh feed

        if refresh:
            st.rerun()
            # Reload UI when clicked

    # =====================================
    # LOAD POSTS FROM BACKEND
    # =====================================
    posts = get_posts(sort_by)
    # Fetch posts depending on sorting option

    # =====================================
    # EMPTY FEED HANDLING
    # =====================================
    if not posts:
        # If no posts exist

        st.info("🌱 No community posts yet.")
        # Inform user feed is empty

        st.write("Be the first to share something!")
        # Encouraging message

        return
        # Stop execution here

    # =====================================
    # FEED HEADER
    # =====================================
    st.markdown("## 📰 Community Feed")
    # Section title

    st.caption(f"{len(posts)} post(s) available")
    # Shows number of posts

    st.markdown("---")
    # Separator

    # =====================================
    # RENDER EACH POST
    # =====================================
    for post in posts:
        # Loop through all posts

        try:
            render_post(
                post,
                user
            )
            # Display each post using render_post()

        except Exception as e:
            # If any post fails to load

            st.error(f"Error loading post: {e}")
            # Show error but continue feed

    # =====================================
    # SIDEBAR SECTION
    # =====================================
    with st.sidebar:
        # Sidebar UI (right side panel)

        st.markdown("## 🌍 Community Rules")

        st.info("""
✅ Be respectful

✅ Share useful content

✅ Help aspirants

❌ No spam

❌ No abusive language
""")
        # Rules shown in info box

        st.markdown("---")

        st.markdown("## 💡 Ideas")
        # Suggestions section

        st.write("• UPSC strategies")
        st.write("• Revision notes")
        st.write("• Motivation")
        st.write("• Current affairs")
        st.write("• Answer writing tips")
        st.write("• PYQ analysis")
        # Idea list for users