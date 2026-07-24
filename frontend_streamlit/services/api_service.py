# =========================================================
# 🌐 API SERVICE (STREAMLIT → FASTAPI CONNECTOR)
# =========================================================

import requests


# =========================================================
# ⚙️ CONFIG
# =========================================================
BASE_URL = "http://127.0.0.1:8000"


# =========================================================
# 📰 GET CURRENT AFFAIRS
# =========================================================
def get_daily_current_affairs(token: str = None):

    try:

        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(
            f"{BASE_URL}/ca/daily",
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            print("[API ERROR]", response.text)
            return []

        data = response.json()

        return data.get("data", [])

    except Exception as e:
        print("[API FAILED]", e)
        return []