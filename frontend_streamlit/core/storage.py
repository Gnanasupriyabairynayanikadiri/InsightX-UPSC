import os
import json

from core.logger import (
    log_info,
    log_error,
    log_exception
)


# =========================================
# BASE DIRECTORY
# =========================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STORAGE_DIR = os.path.join(
    BASE_DIR,
    "storage"
)

os.makedirs(STORAGE_DIR, exist_ok=True)


# =========================================
# FILE PATHS
# =========================================
USERS_FILE = os.path.join(
    STORAGE_DIR,
    "users.json"
)

XP_FILE = os.path.join(
    STORAGE_DIR,
    "xp.json"
)

PROGRESS_FILE = os.path.join(
    STORAGE_DIR,
    "progress.json"
)

LEADERBOARD_FILE = os.path.join(
    STORAGE_DIR,
    "leaderboard.json"
)

COMMUNITY_FILE = os.path.join(
    STORAGE_DIR,
    "community.json"
)

CURRENT_AFFAIRS_FILE = os.path.join(
    STORAGE_DIR,
    "current_affairs.json"
)

DAILY_FILE = os.path.join(
    STORAGE_DIR,
    "daily.json"
)

TOP_ANSWER_FILE = os.path.join(
    STORAGE_DIR,
    "top_answer.json"
)

STUDY_PLAN_FILE = os.path.join(
    STORAGE_DIR,
    "study_plan.json"
)


# =========================================
# SAFE LOAD JSON
# =========================================
def load_json(file_path, default=None):

    if default is None:
        default = {}

    try:

        if not os.path.exists(file_path):

            save_json(file_path, default)

            return default

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        log_error(
            f"JSON corruption detected: {file_path}"
        )

        return default

    except Exception as e:

        log_exception(e)

        return default


# =========================================
# SAFE SAVE JSON
# =========================================
def save_json(file_path, data):

    try:

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        log_exception(e)

        return False


# =========================================
# DELETE FILE
# =========================================
def delete_file(file_path):

    try:

        if os.path.exists(file_path):
            os.remove(file_path)

            log_info(
                f"Deleted file: {file_path}"
            )

            return True

        return False

    except Exception as e:

        log_exception(e)

        return False


# =========================================
# CLEAR JSON FILE
# =========================================
def clear_json(file_path):

    return save_json(file_path, {})


# =========================================
# USERS
# =========================================
def load_users():

    return load_json(
        USERS_FILE,
        {}
    )


def save_users(data):

    return save_json(
        USERS_FILE,
        data
    )


# =========================================
# XP
# =========================================
def load_xp():

    return load_json(
        XP_FILE,
        {}
    )


def save_xp(data):

    return save_json(
        XP_FILE,
        data
    )


# =========================================
# PROGRESS
# =========================================
def load_progress():

    return load_json(
        PROGRESS_FILE,
        {}
    )


def save_progress(data):

    return save_json(
        PROGRESS_FILE,
        data
    )


# =========================================
# LEADERBOARD
# =========================================
def load_leaderboard():

    return load_json(
        LEADERBOARD_FILE,
        {}
    )


def save_leaderboard(data):

    return save_json(
        LEADERBOARD_FILE,
        data
    )


# =========================================
# COMMUNITY
# =========================================
def load_community():

    return load_json(
        COMMUNITY_FILE,
        []
    )


def save_community(data):

    return save_json(
        COMMUNITY_FILE,
        data
    )


# =========================================
# CURRENT AFFAIRS
# =========================================
def load_current_affairs():

    return load_json(
        CURRENT_AFFAIRS_FILE,
        {}
    )


def save_current_affairs(data):

    return save_json(
        CURRENT_AFFAIRS_FILE,
        data
    )


# =========================================
# DAILY
# =========================================
def load_daily():

    return load_json(
        DAILY_FILE,
        {}
    )


def save_daily(data):

    return save_json(
        DAILY_FILE,
        data
    )


# =========================================
# TOP ANSWERS
# =========================================
def load_top_answers():

    return load_json(
        TOP_ANSWER_FILE,
        {}
    )


def save_top_answers(data):

    return save_json(
        TOP_ANSWER_FILE,
        data
    )


# =========================================
# STUDY PLANS
# =========================================
def load_study_plans():

    return load_json(
        STUDY_PLAN_FILE,
        {}
    )


def save_study_plans(data):

    return save_json(
        STUDY_PLAN_FILE,
        data
    )


# =========================================
# GENERIC STORAGE
# =========================================
def get_storage_path(filename):

    return os.path.join(
        STORAGE_DIR,
        filename
    )


def load_generic(filename, default=None):

    path = get_storage_path(filename)

    return load_json(path, default)


def save_generic(filename, data):

    path = get_storage_path(filename)

    return save_json(path, data)