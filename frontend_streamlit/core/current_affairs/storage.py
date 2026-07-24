# =========================================================
# FILE: core/current_affairs/storage.py
# FINAL UPSC CURRENT AFFAIRS STORAGE ENGINE
# =========================================================

import os
import json
from datetime import datetime


# =========================================================
# STORAGE CONFIG
# =========================================================

STORAGE_DIR = "storage/current_affairs"


# =========================================================
# CREATE STORAGE
# =========================================================

def initialize_storage():

    os.makedirs(
        STORAGE_DIR,
        exist_ok=True
    )


# =========================================================
# CURRENT MONTH FILE
# =========================================================

def get_month_file():

    now = datetime.now()

    filename = (
        f"{now.year}_{now.month:02d}.json"
    )

    return os.path.join(
        STORAGE_DIR,
        filename
    )


# =========================================================
# LOAD DATA
# =========================================================

def load_month_data():

    initialize_storage()

    file_path = get_month_file()

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, list):
                return data

            return []

    except Exception as e:

        print(
            "[STORAGE LOAD ERROR]",
            e
        )

        return []


# =========================================================
# SAVE DATA
# =========================================================

def save_month_data(data):

    initialize_storage()

    file_path = get_month_file()

    try:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:

        print(
            "[STORAGE SAVE ERROR]",
            e
        )


# =========================================================
# DUPLICATE CHECK
# =========================================================

def is_duplicate(existing_data, title):

    title = str(title).strip().lower()

    for item in existing_data:

        stored_title = str(

            item.get(
                "title",
                ""
            )

        ).strip().lower()

        if stored_title == title:

            return True

    return False


# =========================================================
# NORMALIZE ITEM
# =========================================================

def normalize_storage_item(news):

    return {

        "date":
            datetime.now().strftime(
                "%Y-%m-%d"
            ),

        "title":
            news.get(
                "title",
                ""
            ),

        "description":
            news.get(
                "description",
                ""
            ),

        "category":
            news.get(
                "category",
                "General Studies"
            ),

        "importance":
            news.get(
                "importance",
                "Medium"
            ),

        "relevance_score":
            news.get(
                "relevance_score",
                0
            ),

        "quick_summary":
            news.get(
                "quick_summary",
                ""
            ),

        "background":
            news.get(
                "background",
                ""
            ),

        "source":
            news.get(
                "source",
                "Unknown"
            ),

        "link":
            news.get(
                "link",
                ""
            ),

        "mains_question":
            news.get(
                "mains_question",
                ""
            ),

        "prelims_focus":
            news.get(
                "prelims_focus",
                []
            ),

        "tags":
            news.get(
                "tags",
                []
            ),

        "pyq_links":
            news.get(
                "pyq_links",
                []
            ),

        "editorial":
            news.get(
                "editorial",
                {}
            ),

        "mcqs":
            news.get(
                "mcqs",
                []
            )
    }


# =========================================================
# STORE CURRENT AFFAIRS
# =========================================================

def store_current_affairs(news_list):

    existing_data = load_month_data()

    updated_data = existing_data.copy()

    for news in news_list:

        title = news.get(
            "title",
            ""
        )

        if not title:
            continue

        if is_duplicate(
            updated_data,
            title
        ):
            continue

        updated_data.append(

            normalize_storage_item(
                news
            )

        )

    updated_data.sort(

        key=lambda x:

        (
            x.get(
                "relevance_score",
                0
            ),

            x.get(
                "date",
                ""
            )
        ),

        reverse=True
    )

    save_month_data(
        updated_data
    )

    return len(updated_data)


# =========================================================
# ALL NEWS
# =========================================================

def get_monthly_current_affairs():

    return load_month_data()


# =========================================================
# TODAY NEWS
# =========================================================

def get_today_current_affairs():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return [

        item

        for item in load_month_data()

        if item.get("date") == today
    ]


# =========================================================
# HIGH IMPORTANCE
# =========================================================

def get_high_importance_news():

    return [

        item

        for item in load_month_data()

        if item.get(
            "importance"
        ) == "High"
    ]


# =========================================================
# CATEGORY FILTER
# =========================================================

def get_news_by_category(category):

    return [

        item

        for item in load_month_data()

        if item.get(
            "category"
        ) == category
    ]


# =========================================================
# TOP UPSC NEWS
# =========================================================

def get_top_news(limit=20):

    data = load_month_data()

    data.sort(

        key=lambda x:
        x.get(
            "relevance_score",
            0
        ),

        reverse=True
    )

    return data[:limit]


# =========================================================
# SEARCH NEWS
# =========================================================

def search_news(keyword):

    keyword = keyword.lower()

    return [

        item

        for item in load_month_data()

        if keyword in
        item.get(
            "title",
            ""
        ).lower()
    ]


# =========================================================
# CLEAR STORAGE
# =========================================================

def clear_current_affairs():

    file_path = get_month_file()

    try:

        if os.path.exists(file_path):

            os.remove(file_path)

            return True

    except Exception as e:

        print(
            "[CLEAR ERROR]",
            e
        )

    return False