# core/pyq_mapper.py


# =========================================================
# 🧠 GS CLASSIFICATION FOR PYQ
# =========================================================
def detect_gs(topic):

    topic = topic.lower()

    if any(k in topic for k in ["constitution", "supreme court", "parliament", "federal"]):
        return "GS2 (Polity & Governance)"

    if any(k in topic for k in ["economy", "rbi", "inflation", "budget"]):
        return "GS3 (Economy)"

    if any(k in topic for k in ["climate", "environment", "biodiversity"]):
        return "GS3 (Environment)"

    if any(k in topic for k in ["history", "culture", "art"]):
        return "GS1 (History & Culture)"

    if any(k in topic for k in ["ethics", "integrity"]):
        return "GS4 (Ethics)"

    return "General Studies"


# =========================================================
# 📘 PYQ PATTERN GENERATOR
# =========================================================
def get_pyq_patterns(topic):

    topic = topic.lower()

    patterns = []

    if "constitution" in topic:
        patterns = [
            "Explain constitutional provisions related to...",
            "Discuss the significance of Article-based governance...",
            "Analyze judicial interpretation in India..."
        ]

    elif "rbi" in topic or "economy" in topic:
        patterns = [
            "Discuss monetary policy tools of RBI",
            "Explain inflation control mechanisms",
            "Impact of fiscal policy on growth"
        ]

    elif "environment" in topic:
        patterns = [
            "Climate change and India’s commitments",
            "Biodiversity conservation measures",
            "Impact of environmental regulations"
        ]

    else:
        patterns = [
            "Explain the concept and its relevance in India",
            "Discuss challenges and reforms needed",
            "Analyze policy implications"
        ]

    return patterns


# =========================================================
# 🧠 MAIN PYQ MAPPER FUNCTION
# =========================================================
def map_pyq(topic):

    gs = detect_gs(topic)
    patterns = get_pyq_patterns(topic)

    return {
        "topic": topic,
        "gs_paper": gs,

        # UPSC intelligence layer
        "pyq_trend": f"{topic} is repeatedly asked in UPSC under analytical and application-based questions.",

        "question_patterns": patterns,

        "probable_future_question": f"Critically analyze the role of {topic} in contemporary Indian governance and development.",

        "keywords": topic.split(),

        "difficulty": "Medium to High"
    }


# =========================================================
# 🧪 TEST
# =========================================================
if __name__ == "__main__":

    print(map_pyq("RBI monetary policy"))