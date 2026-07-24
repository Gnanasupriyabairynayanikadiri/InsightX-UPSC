# =====================================================
# 🧠 UPSC AI STUDY PLANNER ENGINE
# =====================================================

import random
from datetime import date

SUBJECTS = ["Polity", "History", "Geography", "Economy", "CSAT", "Current Affairs"]


def generate_ai_plan(user_data=None):

    plan = []

    base_blocks = [
        ("📚 NCERT Revision", 60),
        ("🧠 MCQ Practice", 45),
        ("📰 Current Affairs", 40),
        ("✍️ Answer Writing", 60),
        ("🔁 Revision Block", 45),
    ]

    for task, duration in base_blocks:

        plan.append({
            "task": task,
            "duration": duration,
            "priority": random.randint(1, 3),
            "done": False
        })

    return {
        "date": str(date.today()),
        "tasks": plan
    }