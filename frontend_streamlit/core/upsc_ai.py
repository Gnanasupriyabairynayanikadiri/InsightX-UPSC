# core/upsc_ai.py

import re
from datetime import datetime
from core.logger import log_error


# =========================================================
# 🧠 GS CLASSIFICATION ENGINE
# =========================================================
def classify_gs(text):
    text = text.lower()

    if any(k in text for k in ["constitution", "supreme court", "parliament", "bill", "article"]):
        return "GS2"

    if any(k in text for k in ["economy", "rbi", "inflation", "budget", "gdp"]):
        return "GS3"

    if any(k in text for k in ["climate", "environment", "biodiversity", "pollution"]):
        return "GS3"

    if any(k in text for k in ["history", "culture", "heritage"]):
        return "GS1"

    if any(k in text for k in ["ethics", "integrity", "governance"]):
        return "GS4"

    return "GS2"


# =========================================================
# 📂 SYLLABUS TAGGING
# =========================================================
def get_syllabus_tag(text):
    text = text.lower()

    mapping = {
        "Judiciary": ["supreme court", "high court", "judgement"],
        "Polity": ["constitution", "parliament", "election"],
        "Economy": ["rbi", "inflation", "budget"],
        "Environment": ["climate", "pollution", "biodiversity"],
        "Science & Tech": ["isro", "ai", "satellite"]
    }

    for tag, keywords in mapping.items():
        for k in keywords:
            if k in text:
                return tag

    return "General Studies"


# =========================================================
# 🎯 IMPORTANCE SCORING ENGINE
# =========================================================
def get_importance(text):
    text = text.lower()

    high = ["supreme court", "rbi", "constitution", "budget", "climate summit"]

    medium = ["india", "policy", "agreement", "reform", "mission"]

    if any(k in text for k in high):
        return "High"
    if any(k in text for k in medium):
        return "Medium"

    return "Low"


# =========================================================
# ✍️ MAINS ANSWER GENERATOR (STATIC UPSC STYLE)
# =========================================================
def generate_mains_summary(article):
    try:
        title = article.get("title", "")
        content = article.get("content", "")

        return f"""
The news regarding {title} is significant from the UPSC perspective.

This development highlights important issues related to governance, policy implementation, and institutional functioning in India.

It reflects the evolving nature of India's administrative and socio-economic framework.

Such developments are important for both GS syllabus understanding and analytical answer writing in Mains examination.
""".strip()

    except Exception as e:
        log_error(f"Mains generation error: {e}")
        return "No summary available."


# =========================================================
# ❓ PRELIMS MCQ GENERATOR (RULE BASED)
# =========================================================
def generate_mcq(article):

    title = article.get("title", "")

    return {
        "question": f"Which of the following is most relevant to: {title}?",
        "options": [
            "Governance and Policy Framework",
            "International Trade only",
            "Sports Development",
            "None of the above"
        ],
        "answer": "Governance and Policy Framework"
    }


# =========================================================
# 🧠 MAIN AI PIPELINE FUNCTION
# =========================================================
def analyze_article(article):

    try:

        text = article.get("title", "") + " " + article.get("content", "")

        return {
            "title": article.get("title"),
            "content": article.get("content"),
            "source": article.get("source"),
            "published": article.get("published"),
            "url": article.get("url"),

            # 🧠 UPSC INTELLIGENCE LAYER
            "gs_paper": classify_gs(text),
            "tag": get_syllabus_tag(text),
            "importance": get_importance(text),

            # ✍️ OUTPUTS
            "mains_summary": generate_mains_summary(article),
            "prelims_mcq": generate_mcq(article),

            "created_at": datetime.now().strftime("%Y-%m-%d")
        }

    except Exception as e:
        log_error(f"AI analysis failed: {e}")
        return None


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":

    sample = {
        "title": "Supreme Court delivers landmark verdict",
        "content": "The Supreme Court ruled on constitutional validity.",
        "source": "The Hindu",
        "published": "2026-05-15"
    }

    print(analyze_article(sample))