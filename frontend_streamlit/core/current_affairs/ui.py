import streamlit as st
import requests
import pandas as pd


# =========================================================
# CONFIG
# =========================================================

API_URL = "https://insightx-upsc-production.up.railway.app"


# =========================================================
# FETCH DATA
# =========================================================

def fetch_current_affairs():

    try:

        response = requests.get(
            f"{API_URL}/ca/daily",
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        

        return data.get("data", [])

    except Exception as e:

        st.error(f"API Error: {e}")

        return []


# =========================================================
# FILTERS
# =========================================================

def render_filters(df):

    st.sidebar.header("🎯 Filters")

    category = st.sidebar.selectbox(
        "Category",
        ["All"]
        + sorted(
            df["category"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    importance = st.sidebar.selectbox(
        "Importance",
        ["All", "High", "Medium", "Low"]
    )

    min_upsc_score = st.sidebar.slider(
        "Minimum UPSC Score",
        0,
        100,
        50
    )

    return (
        category,
        importance,
        min_upsc_score
    )


# =========================================================
# DASHBOARD METRICS
# =========================================================

def render_metrics(df):

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Articles",
        len(df)
    )

    col2.metric(
        "High Importance",
        len(
            df[
                df["importance"]
                == "High"
            ]
        )
    )

    col3.metric(
        "Avg Relevance",
        round(
            df["relevance_score"].mean(),
            2
        )
        if len(df)
        else 0
    )

    col4.metric(
        "Avg UPSC Score",
        round(
            df["upsc_score"].mean(),
            2
        )
        if len(df)
        else 0
    )


# =========================================================
# TOP PRIORITY TOPICS
# =========================================================

def render_top_topics(df):

    st.header("🔥 Today's Top UPSC Topics")

    top = df.sort_values(
        by="upsc_score",
        ascending=False
    ).head(5)

    for _, row in top.iterrows():

        st.write(
            f"⭐ {row['title']} "
            f"(Score: {row['upsc_score']})"
        )

    st.divider()


# =========================================================
# NEWS CARD
# =========================================================

def render_news_card(item):

    st.subheader(
        item.get("title", "Untitled")
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.write(
        f"📌 {item.get('category','-')}"
    )

    c2.write(
        f"🔥 {item.get('importance','-')}"
    )

    c3.write(
        f"⭐ {item.get('relevance_score',0)}"
    )

    c4.write(
        f"🎯 {item.get('upsc_score',0)}"
    )

    summary = item.get(
        "quick_summary",
        ""
    )

    if summary:
        st.info(summary)

    insight = item.get(
        "insight",
        ""
    )

    if insight:
        st.success(
            f"🧠 UPSC Insight: {insight}"
        )

    with st.expander(
        "📖 Full Analysis"
    ):

        st.write("### GS Paper")

        st.write(
            item.get(
                "gs_paper",
                ""
            )
        )

        st.write("### Description")

        st.write(
            item.get(
                "description",
                ""
            )
        )

        st.write("### Background")

        st.write(
            item.get(
                "background",
                ""
            )
        )

        st.write("### Prelims Focus")

        prelims = item.get(
            "prelims_focus",
            []
        )

        if isinstance(
            prelims,
            list
        ):
            for p in prelims:
                st.write(f"• {p}")

        st.write("### Mains Question")

        st.success(
            item.get(
                "mains_question",
                ""
            )
        )

        tags = item.get(
            "tags",
            []
        )

        if tags:

            st.write("### Tags")

            st.write(
                ", ".join(tags)
            )

        pyqs = item.get(
            "pyq_links",
            []
        )

        if pyqs:

            st.write(
                "### Related PYQs"
            )

            for pyq in pyqs:

                st.write(
                    f"• {pyq}"
                )

        st.write("### Source")

        st.write(
            item.get(
                "source",
                ""
            )
        )

        link = item.get(
            "link",
            ""
        )

        if link:
            st.markdown(
                f"[Read Original Article]({link})"
            )

    st.markdown("---")


# =========================================================
# REVISION SECTION
# =========================================================

def render_revision_section(news):

    st.header(
        "📚 Revision Focus"
    )

    categories = {}

    for item in news:

        category = item.get(
            "category",
            "General Studies"
        )

        categories[category] = (
            categories.get(
                category,
                0
            )
            + 1
        )

    for category, count in categories.items():

        st.write(
            f"• Revise {category} "
            f"({count} topics)"
        )


# =========================================================
# MAIN PAGE
# =========================================================

def current_affairs_ui(user=None):

    st.title(
        "🧠 UPSC Current Affairs Intelligence Feed"
    )

    news = fetch_current_affairs()
    

    if not news:

        st.warning(
            "No Current Affairs Found"
        )

        return

    df = pd.DataFrame(news)

    defaults = {
        "category": "General",
        "importance": "Medium",
        "relevance_score": 0,
        "upsc_score": 0
    }

    for col, val in defaults.items():

        if col not in df.columns:
            df[col] = val

    category, importance, min_score = render_filters(df)

    if category != "All":

        df = df[
            df["category"]
            == category
        ]

    if importance != "All":

        df = df[
            df["importance"]
            == importance
        ]

    df = df[
        df["upsc_score"]
        >= min_score
    ]

    render_metrics(df)

    render_top_topics(df)

    for _, row in df.iterrows():

        render_news_card(
            row.to_dict()
        )

    render_revision_section(
        df.to_dict(
            orient="records"
        )
    )