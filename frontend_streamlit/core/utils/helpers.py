# =========================================================
# FILE: core/utils/helpers.py
# =========================================================

def safe_get(data, key, default=""):

    try:

        value = data.get(key, default)

        if value is None:
            return default

        return value

    except Exception:
        return default