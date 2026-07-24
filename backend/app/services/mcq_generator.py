import random


def generate_mcq(title: str, category: str):

    # -----------------------------------------------------
    # SIMPLE AI-STYLE UPSC MCQ GENERATION LOGIC
    # (Later can be replaced with LLM)
    # -----------------------------------------------------

    options_pool = [
        "Economic Policy",
        "International Relations",
        "Science & Technology",
        "Environment",
        "Polity"
    ]

    correct = category if category in options_pool else random.choice(options_pool)

    options = list(set([
        correct,
        random.choice(options_pool),
        random.choice(options_pool),
        random.choice(options_pool)
    ]))

    random.shuffle(options)

    return {
        "question": f"With reference to {title}, consider the following context:",
        "options": options,
        "answer": correct,
        "explanation": f"This relates to {category} which is important for UPSC."
    }
