import os
import logging

from datetime import datetime


# =========================================
# LOG DIRECTORY
# =========================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

os.makedirs(LOG_DIR, exist_ok=True)


# =========================================
# LOG FILES
# =========================================
APP_LOG_FILE = os.path.join(
    LOG_DIR,
    "app.log"
)

ERROR_LOG_FILE = os.path.join(
    LOG_DIR,
    "error.log"
)


# =========================================
# LOGGER FORMAT
# =========================================
LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =========================================
# CREATE LOGGER
# =========================================
def create_logger(name="InsightX"):

    logger = logging.getLogger(name)

    # prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # =====================================
    # CONSOLE HANDLER
    # =====================================
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # =====================================
    # FILE HANDLER
    # =====================================
    file_handler = logging.FileHandler(
        APP_LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # =====================================
    # ERROR FILE HANDLER
    # =====================================
    error_handler = logging.FileHandler(
        ERROR_LOG_FILE,
        encoding="utf-8"
    )

    error_handler.setLevel(logging.ERROR)

    error_handler.setFormatter(formatter)

    logger.addHandler(error_handler)

    return logger


# =========================================
# GLOBAL LOGGER
# =========================================
logger = create_logger()


# =========================================
# INFO
# =========================================
def log_info(message):

    logger.info(message)


# =========================================
# DEBUG
# =========================================
def log_debug(message):

    logger.debug(message)


# =========================================
# WARNING
# =========================================
def log_warning(message):

    logger.warning(message)


# =========================================
# ERROR
# =========================================
def log_error(message):

    logger.error(message)


# =========================================
# CRITICAL
# =========================================
def log_critical(message):

    logger.critical(message)


# =========================================
# EXCEPTION LOGGER
# =========================================
def log_exception(error):

    logger.exception(error)


# =========================================
# USER ACTION LOGGER
# =========================================
def log_user_action(user, action):

    logger.info(
        f"[USER ACTION] {user} -> {action}"
    )


# =========================================
# API LOGGER
# =========================================
def log_api(api_name, status):

    logger.info(
        f"[API] {api_name} -> {status}"
    )


# =========================================
# QUIZ LOGGER
# =========================================
def log_quiz(user, chapter, score):

    logger.info(
        f"[QUIZ] {user} | {chapter} | Score={score}"
    )


# =========================================
# ANSWER WRITING LOGGER
# =========================================
def log_answer(user, question, score):

    logger.info(
        f"[ANSWER] {user} | Score={score}"
    )


# =========================================
# DAILY LOG SEPARATOR
# =========================================
def log_separator():

    logger.info(
        "=" * 60
    )


# =========================================
# STARTUP LOG
# =========================================
log_separator()

logger.info(
    f"🚀 InsightX Logger Started @ {datetime.now()}"
)

log_separator()