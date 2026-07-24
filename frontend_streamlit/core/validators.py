import re

from core.utils import (
    clean_text,
    word_count,
    safe_int
)

from core.constants import (
    MIN_ANSWER_WORDS,
    MAX_ANSWER_WORDS
)


# =========================================
# USERNAME VALIDATION
# =========================================
def validate_username(username):

    username = clean_text(username)

    if not username:
        return False, "Username cannot be empty"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    if len(username) > 20:
        return False, "Username too long"

    if not username.replace("_", "").isalnum():
        return False, "Only letters, numbers, underscore allowed"

    return True, "Valid username"


# =========================================
# PASSWORD VALIDATION
# =========================================
def validate_password(password):

    if not password:
        return False, "Password required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    if len(password) > 50:
        return False, "Password too long"

    return True, "Valid password"


# =========================================
# EMAIL VALIDATION
# =========================================
def validate_email(email):

    email = clean_text(email)

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if re.match(pattern, email):
        return True, "Valid email"

    return False, "Invalid email"


# =========================================
# EMPTY TEXT CHECK
# =========================================
def validate_text(text):

    text = clean_text(text)

    if not text:
        return False, "Text cannot be empty"

    return True, "Valid text"


# =========================================
# ANSWER VALIDATION
# =========================================
def validate_answer(answer):

    answer = clean_text(answer)

    if not answer:
        return False, "Answer cannot be empty"

    words = word_count(answer)

    if words < MIN_ANSWER_WORDS:
        return (
            False,
            f"Minimum {MIN_ANSWER_WORDS} words required"
        )

    if words > MAX_ANSWER_WORDS:
        return (
            False,
            f"Maximum {MAX_ANSWER_WORDS} words allowed"
        )

    return True, "Valid answer"


# =========================================
# QUIZ OPTION VALIDATION
# =========================================
def validate_quiz_question(question):

    required = [
        "question",
        "options",
        "answer"
    ]

    if not isinstance(question, dict):
        return False, "Question must be dictionary"

    for key in required:

        if key not in question:
            return False, f"Missing key: {key}"

    options = question.get("options", [])

    if not isinstance(options, list):
        return False, "Options must be list"

    if len(options) < 2:
        return False, "Minimum 2 options required"

    if question["answer"] not in options:
        return False, "Answer not present in options"

    return True, "Valid question"


# =========================================
# FILE TYPE VALIDATION
# =========================================
def validate_image_file(filename):

    if not filename:
        return False, "No file selected"

    allowed = [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]

    filename = filename.lower()

    for ext in allowed:

        if filename.endswith(ext):
            return True, "Valid image"

    return False, "Unsupported image format"


# =========================================
# FILE SIZE VALIDATION
# =========================================
def validate_file_size(size_mb, max_size=5):

    size_mb = safe_int(size_mb)

    if size_mb > max_size:
        return (
            False,
            f"File too large (max {max_size}MB)"
        )

    return True, "Valid size"


# =========================================
# POSITIVE NUMBER
# =========================================
def validate_positive_number(value):

    try:

        value = float(value)

        if value < 0:
            return False, "Must be positive"

        return True, "Valid number"

    except:
        return False, "Invalid number"


# =========================================
# RANGE VALIDATION
# =========================================
def validate_range(value, minimum, maximum):

    try:

        value = float(value)

        if value < minimum:
            return (
                False,
                f"Minimum allowed is {minimum}"
            )

        if value > maximum:
            return (
                False,
                f"Maximum allowed is {maximum}"
            )

        return True, "Valid range"

    except:
        return False, "Invalid value"


# =========================================
# URL VALIDATION
# =========================================
def validate_url(url):

    pattern = (
        r"^(https?:\/\/)?"
        r"([\da-z\.-]+)\."
        r"([a-z\.]{2,6})"
        r"([\/\w \.-]*)*\/?$"
    )

    if re.match(pattern, url):
        return True, "Valid URL"

    return False, "Invalid URL"


# =========================================
# DATE VALIDATION
# =========================================
def validate_date(date_text):

    pattern = r"^\d{4}-\d{2}-\d{2}$"

    if re.match(pattern, date_text):
        return True, "Valid date"

    return False, "Invalid date format"


# =========================================
# SAFE BOOLEAN
# =========================================
def validate_boolean(value):

    if isinstance(value, bool):
        return True, "Valid boolean"

    return False, "Invalid boolean"


# =========================================
# LIST VALIDATION
# =========================================
def validate_list(data):

    if isinstance(data, list):
        return True, "Valid list"

    return False, "Invalid list"


# =========================================
# DICTIONARY VALIDATION
# =========================================
def validate_dict(data):

    if isinstance(data, dict):
        return True, "Valid dictionary"

    return False, "Invalid dictionary"