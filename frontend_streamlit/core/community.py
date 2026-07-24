# =========================================================
# 📁 FILE: core/community.py
# =========================================================

import streamlit as st
import json
import os
import uuid

from datetime import datetime

from core.xp import add_xp


# =========================================================
# STORAGE
# =========================================================
FILE = "storage/community.json"

IMAGE_FOLDER = "storage/community_images"


# =========================================================
# ENSURE STORAGE
# =========================================================
def ensure_storage():

    os.makedirs("storage", exist_ok=True)

    os.makedirs(
        IMAGE_FOLDER,
        exist_ok=True
    )

    if not os.path.exists(FILE):

        with open(
            FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump([], f)


# =========================================================
# LOAD DATA
# =========================================================
def load_data():

    ensure_storage()

    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, list):
                return data

            return []

    except:
        return []


# =========================================================
# SAVE DATA
# =========================================================
def save_data(data):

    ensure_storage()

    if not isinstance(data, list):
        data = []

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# SAVE IMAGE
# =========================================================
def save_image(image):

    if image is None:
        return None

    ensure_storage()

    filename = f"""
{uuid.uuid4()}_{image.name}
"""

    path = os.path.join(
        IMAGE_FOLDER,
        filename
    )

    with open(path, "wb") as f:

        f.write(image.getbuffer())

    return path


# =========================================================
# FORMAT DATE
# =========================================================
def format_date(date):

    try:

        dt = datetime.fromisoformat(date)

        return dt.strftime(
            "%d %b %Y | %I:%M %p"
        )

    except:
        return date


# =========================================================
# ADD POST
# =========================================================
def add_post(

    user,
    content,
    image=None,
    tags=None,
    score=None

):

    if not content.strip() and image is None:
        return False

    data = load_data()

    post = {

        "id": str(uuid.uuid4()),

        "user": user,

        "content": content.strip(),

        "image": save_image(image),

        "likes": 0,

        "liked_by": [],

        "comments": [],

        "score": score,

        "tags": tags if tags else [],

        "date": str(datetime.now())
    }

    data.append(post)

    save_data(data)

    # =====================================================
    # XP
    # =====================================================
    try:
        add_xp(user, 3)
    except:
        pass

    return True


# =========================================================
# DELETE POST
# =========================================================
def delete_post(post_id, user):

    data = load_data()

    updated = []

    for post in data:

        if (

            post["id"] == post_id

            and

            post["user"] == user

        ):

            image = post.get("image")

            if (

                image

                and

                os.path.exists(image)

            ):

                try:
                    os.remove(image)
                except:
                    pass

        else:

            updated.append(post)

    save_data(updated)


# =========================================================
# EDIT POST
# =========================================================
def edit_post(

    post_id,
    user,
    new_content

):

    data = load_data()

    for post in data:

        if (

            post["id"] == post_id

            and

            post["user"] == user

        ):

            post["content"] = new_content.strip()

            break

    save_data(data)


# =========================================================
# LIKE POST
# =========================================================
def like_post(post_id, user):

    data = load_data()

    for post in data:

        if post["id"] == post_id:

            if user not in post["liked_by"]:

                post["likes"] += 1

                post["liked_by"].append(user)

            else:

                post["likes"] -= 1

                post["liked_by"].remove(user)

            break

    save_data(data)


# =========================================================
# ADD COMMENT
# =========================================================
def add_comment(

    post_id,
    user,
    text

):

    if not text.strip():
        return

    data = load_data()

    for post in data:

        if post["id"] == post_id:

            post["comments"].append({

                "user": user,

                "text": text.strip(),

                "date": str(datetime.now())
            })

            break

    save_data(data)

    try:
        add_xp(user, 1)
    except:
        pass


# =========================================================
# GET POSTS
# =========================================================
def get_posts(sort_by="Latest"):

    data = load_data()

    # =====================================================
    # MOST LIKED
    # =====================================================
    if sort_by == "Most Liked":

        return sorted(

            data,

            key=lambda x: x.get(
                "likes",
                0
            ),

            reverse=True
        )

    # =====================================================
    # TOP SCORES
    # =====================================================
    if sort_by == "Top Answers":

        return sorted(

            data,

            key=lambda x: x.get(
                "score",
                0
            ) if x.get("score") else 0,

            reverse=True
        )

    # =====================================================
    # LATEST
    # =====================================================
    return sorted(

        data,

        key=lambda x: x.get(
            "date",
            ""
        ),

        reverse=True
    )


# =========================================================
# RENDER POST
# =========================================================
def render_post(post, user):

    with st.container():

        st.markdown("""
---
""")

        # =================================================
        # HEADER
        # =================================================
        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(
                f"### 👤 {post['user']}"
            )

        with col2:

            if post.get("score"):

                st.success(
                    f"🏆 {post['score']}/10"
                )

        # =================================================
        # TAGS
        # =================================================
        tags = post.get("tags", [])

        if tags:

            st.caption(
                " • ".join(tags)
            )

        # =================================================
        # DATE
        # =================================================
        st.caption(
            format_date(
                post.get("date", "")
            )
        )

        # =================================================
        # CONTENT
        # =================================================
        st.write(
            post.get("content", "")
        )

        # =================================================
        # IMAGE
        # =================================================
        if post.get("image"):

            try:

                st.image(
                    post["image"],
                    use_container_width=True
                )

            except:

                st.warning(
                    "Image unavailable"
                )

        # =================================================
        # ACTIONS
        # =================================================
        c1, c2, c3 = st.columns([1, 1, 5])

        # =================================================
        # LIKE
        # =================================================
        with c1:

            liked = user in post.get(
                "liked_by",
                []
            )

            btn = "❤️" if liked else "🤍"

            if st.button(

                f"{btn} {post.get('likes', 0)}",

                key=f"""
like_{post['id']}
"""
            ):

                like_post(
                    post["id"],
                    user
                )

                st.rerun()

        # =================================================
        # DELETE
        # =================================================
        with c2:

            if post["user"] == user:

                if st.button(

                    "🗑️",

                    key=f"""
delete_{post['id']}
"""
                ):

                    delete_post(
                        post["id"],
                        user
                    )

                    st.rerun()

        # =================================================
        # COMMENTS
        # =================================================
        comments = post.get(
            "comments",
            []
        )

        if comments:

            with st.expander(

                f"💬 Comments ({len(comments)})"
            ):

                for c in comments:

                    st.markdown(f"""
**{c['user']}**

{c['text']}

🕒 {format_date(c['date'])}

---
""")

        # =================================================
        # ADD COMMENT
        # =================================================
        comment = st.text_input(

            "Write a comment",

            key=f"""
comment_{post['id']}
"""
        )

        if st.button(

            "💬 Add Comment",

            key=f"""
commentbtn_{post['id']}
"""
        ):

            add_comment(

                post["id"],

                user,

                comment
            )

            st.rerun()