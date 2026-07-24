# =========================================================
# 📁 FILE: core/map_engine.py
# AI UPSC MAP QUIZ ENGINE
# =========================================================

import random


# =========================================================
# 🌍 WORLD IMPORTS
# =========================================================
from data.map.world.world_capitals import (
    WORLD_CAPITALS_QUESTIONS
)

from data.map.world.world_continents import (
    WORLD_CONTINENTS_QUESTIONS
)

from data.map.world.world_straits import (
    WORLD_STRAITS_QUESTIONS
)

from data.map.world.world_rivers import (
    WORLD_RIVERS_QUESTIONS
)

from data.map.world.world_mountains import (
    WORLD_MOUNTAINS_QUESTIONS
)

from data.map.world.world_geo_politics import (
    WORLD_GEO_POLITICS_QUESTIONS
)


# =========================================================
# 🇮🇳 INDIA IMPORTS
# =========================================================
from data.map.india.indian_states import (
    INDIAN_STATES_QUESTIONS
)

from data.map.india.indian_rivers import (
    INDIAN_RIVERS_QUESTIONS
)

from data.map.india.indian_mountains import (
    INDIAN_MOUNTAINS_QUESTIONS
)

from data.map.india.indian_cities import (
    INDIAN_CITIES_QUESTIONS
)

from data.map.india.indian_geo_politics import (
    INDIAN_GEO_POLITICS_QUESTIONS
)

from data.map.india.indian_biosphere_reserves import (
    INDIAN_BIOSPHERE_RESERVES_QUESTIONS
)


# =========================================================
# 🌍 ALL QUESTIONS
# =========================================================
ALL_QUESTIONS = (

    WORLD_CAPITALS_QUESTIONS +

    WORLD_CONTINENTS_QUESTIONS +

    WORLD_STRAITS_QUESTIONS +

    WORLD_RIVERS_QUESTIONS +

    WORLD_MOUNTAINS_QUESTIONS +

    WORLD_GEO_POLITICS_QUESTIONS +

    INDIAN_STATES_QUESTIONS +

    INDIAN_RIVERS_QUESTIONS +

    INDIAN_MOUNTAINS_QUESTIONS +

    INDIAN_CITIES_QUESTIONS +

    INDIAN_GEO_POLITICS_QUESTIONS +

    INDIAN_BIOSPHERE_RESERVES_QUESTIONS
)


# =========================================================
# 🎯 GENERATE QUESTION
# =========================================================
def generate_map_question(topic="Mixed Quiz"):

    # =====================================================
    # WORLD CAPITALS
    # =====================================================
    if topic == "World Capitals":

        return random.choice(
            WORLD_CAPITALS_QUESTIONS
        )

    # =====================================================
    # CONTINENTS
    # =====================================================
    elif topic == "Continents":

        return random.choice(
            WORLD_CONTINENTS_QUESTIONS
        )

    # =====================================================
    # STRAITS
    # =====================================================
    elif topic == "World Straits":

        return random.choice(
            WORLD_STRAITS_QUESTIONS
        )

    # =====================================================
    # WORLD RIVERS
    # =====================================================
    elif topic == "World Rivers":

        return random.choice(
            WORLD_RIVERS_QUESTIONS
        )

    # =====================================================
    # WORLD MOUNTAINS
    # =====================================================
    elif topic == "World Mountains":

        return random.choice(
            WORLD_MOUNTAINS_QUESTIONS
        )

    # =====================================================
    # GEOPOLITICS
    # =====================================================
    elif topic == "Geopolitics":

        geo_questions = (

            WORLD_GEO_POLITICS_QUESTIONS +

            INDIAN_GEO_POLITICS_QUESTIONS
        )

        return random.choice(
            geo_questions
        )

    # =====================================================
    # INDIAN STATES
    # =====================================================
    elif topic == "Indian States":

        return random.choice(
            INDIAN_STATES_QUESTIONS
        )

    # =====================================================
    # INDIAN RIVERS
    # =====================================================
    elif topic == "Indian Rivers":

        return random.choice(
            INDIAN_RIVERS_QUESTIONS
        )

    # =====================================================
    # INDIAN MOUNTAINS
    # =====================================================
    elif topic == "Indian Mountains":

        return random.choice(
            INDIAN_MOUNTAINS_QUESTIONS
        )

    # =====================================================
    # INDIAN CITIES
    # =====================================================
    elif topic == "Indian Cities":

        return random.choice(
            INDIAN_CITIES_QUESTIONS
        )

    # =====================================================
    # BIOSPHERE RESERVES
    # =====================================================
    elif topic == "Biosphere Reserves":

        return random.choice(
            INDIAN_BIOSPHERE_RESERVES_QUESTIONS
        )

    # =====================================================
    # MIXED QUIZ
    # =====================================================
    return random.choice(
        ALL_QUESTIONS
    )


# =========================================================
# ✅ EVALUATE ANSWER
# =========================================================
def evaluate_answer(

    selected_answer,
    correct_answer
):

    return (

        selected_answer.strip().lower()

        ==

        correct_answer.strip().lower()
    )


# =========================================================
# 💡 QUESTION EXPLANATION
# =========================================================
def get_question_explanation(question):

    # =====================================================
    # DIRECT EXPLANATION
    # =====================================================
    if "explanation" in question:

        return question["explanation"]

    # =====================================================
    # FALLBACK
    # =====================================================
    topic = question.get(
        "topic",
        "Geography"
    )

    answer = question.get(
        "answer",
        ""
    )

    return (

        f"This question belongs to "
        f"'{topic}' and the correct "
        f"answer is '{answer}'. "
        f"It is important for UPSC "
        f"Prelims Geography and Mapping."
    )


# =========================================================
# 🎨 DIFFICULTY COLOR
# =========================================================
def get_difficulty_color(level):

    if level == "Easy":

        return "🟢"

    elif level == "Medium":

        return "🟡"

    elif level == "Hard":

        return "🔴"

    return "⚪"


# =========================================================
# 📊 SCORE ANALYSIS
# =========================================================
def generate_score_analysis(

    score,
    total
):

    # =====================================================
    # SAFETY
    # =====================================================
    if total <= 0:

        return {

            "score": 0,

            "total": 0,

            "percentage": 0,

            "level": "Starter",

            "feedback":
                "Start solving questions."
        }

    # =====================================================
    # PERCENTAGE
    # =====================================================
    percentage = round(

        (score / total) * 100,
        2
    )

    # =====================================================
    # PERFORMANCE
    # =====================================================
    if percentage >= 85:

        level = "Excellent"

        feedback = (

            "Outstanding mapping "
            "and geography skills."
        )

    elif percentage >= 70:

        level = "Good"

        feedback = (

            "Strong preparation. "
            "Revise weak areas."
        )

    elif percentage >= 50:

        level = "Average"

        feedback = (

            "Need more practice "
            "in maps and locations."
        )

    else:

        level = "Weak"

        feedback = (

            "Focus on atlas revision "
            "and daily practice."
        )

    # =====================================================
    # RETURN
    # =====================================================
    return {

        "score": score,

        "total": total,

        "percentage": percentage,

        "level": level,

        "feedback": feedback
    }


# =========================================================
# 📚 GET QUESTIONS BY DIFFICULTY
# =========================================================
def get_questions_by_difficulty(level):

    return [

        q for q in ALL_QUESTIONS

        if q.get(
            "difficulty",
            "Easy"
        ) == level
    ]


# =========================================================
# 📂 GET QUESTIONS BY TOPIC
# =========================================================
def get_questions_by_topic(topic):

    return [

        q for q in ALL_QUESTIONS

        if q.get(
            "topic",
            ""
        ).lower() == topic.lower()
    ]


# =========================================================
# 📈 QUESTION COUNT
# =========================================================
def get_total_question_count():

    return len(
        ALL_QUESTIONS
    )


# =========================================================
# 🌍 AVAILABLE QUIZ TOPICS
# =========================================================
AVAILABLE_MAP_TOPICS = [

    "World Capitals",

    "Continents",

    "World Straits",

    "World Rivers",

    "World Mountains",

    "Indian States",

    "Indian Rivers",

    "Indian Mountains",

    "Indian Cities",

    "Biosphere Reserves",

    "Geopolitics",

    "Mixed Quiz"
]