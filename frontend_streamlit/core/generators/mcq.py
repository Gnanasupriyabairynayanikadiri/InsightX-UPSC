# =========================================================
# 📁 FILE: core/ca_mcq_generator.py
# AI UPSC CURRENT AFFAIRS MCQ GENERATOR
# FINAL UPSC ANALYTICAL VERSION
# =========================================================

import random


# =========================================================
# GENERATE UPSC MCQS
# =========================================================
def generate_mcqs(title, category):

    title = title.strip()

    # =====================================================
    # POLITY MCQS
    # =====================================================
    if category == "Polity":

        return [

            {
                "question":

                f"The issue regarding '{title}' is mainly associated with:",

                "options": [

                    "Constitutional governance",
                    "Wildlife conservation",
                    "Ocean currents",
                    "Volcanic activity"
                ],

                "answer":
                "Constitutional governance",

                "explanation":

                "The topic is related to governance, "
                "constitutional institutions, democratic "
                "accountability, and public administration."
            },

            {
                "question":

                "Which of the following is most important "
                "for strengthening democratic governance?",

                "options": [

                    "Transparency and accountability",
                    "Monopoly powers",
                    "Trade restrictions",
                    "Military rule"
                ],

                "answer":
                "Transparency and accountability",

                "explanation":

                "Transparency and accountability are core "
                "principles of democratic governance."
            }
        ]

    # =====================================================
    # ECONOMY MCQS
    # =====================================================
    elif category == "Economy":

        return [

            {
                "question":

                f"'{title}' is important mainly because of:",

                "options": [

                    "Economic and fiscal implications",
                    "Ancient architecture",
                    "Volcanic eruptions",
                    "Forest conservation"
                ],

                "answer":
                "Economic and fiscal implications",

                "explanation":

                "The issue is linked with economic governance, "
                "taxation, growth, fiscal management, "
                "and development."
            },

            {
                "question":

                "Which of the following is most essential "
                "for sustainable economic growth?",

                "options": [

                    "Investment and productive employment",
                    "Political instability",
                    "Declining literacy",
                    "Trade isolation"
                ],

                "answer":
                "Investment and productive employment",

                "explanation":

                "Investment and employment generation are "
                "important drivers of sustainable growth."
            }
        ]

    # =====================================================
    # INTERNATIONAL RELATIONS MCQS
    # =====================================================
    elif category == "International Relations":

        return [

            {
                "question":

                f"The issue regarding '{title}' is significant because of:",

                "options": [

                    "Strategic and geopolitical relevance",
                    "Agricultural taxation",
                    "Wildlife migration",
                    "Local sports administration"
                ],

                "answer":
                "Strategic and geopolitical relevance",

                "explanation":

                "The topic relates to India's foreign policy, "
                "strategic interests, and geopolitical developments."
            },

            {
                "question":

                "Which of the following is important "
                "for maintaining regional stability?",

                "options": [

                    "Diplomatic cooperation",
                    "Trade embargoes only",
                    "Isolationism",
                    "Military dictatorship"
                ],

                "answer":
                "Diplomatic cooperation",

                "explanation":

                "Diplomatic engagement and strategic cooperation "
                "help maintain regional stability."
            }
        ]

    # =====================================================
    # ENVIRONMENT MCQS
    # =====================================================
    elif category == "Environment":

        return [

            {
                "question":

                f"The issue concerning '{title}' is mainly related to:",

                "options": [

                    "Environmental sustainability",
                    "Corporate taxation",
                    "Electoral reforms",
                    "Ancient literature"
                ],

                "answer":
                "Environmental sustainability",

                "explanation":

                "The topic concerns ecological balance, "
                "climate governance, biodiversity, "
                "and sustainability."
            },

            {
                "question":

                "Which principle is important in "
                "environmental governance?",

                "options": [

                    "Polluter Pays Principle",
                    "Military Rule Principle",
                    "Colonial Principle",
                    "Trade Monopoly Principle"
                ],

                "answer":
                "Polluter Pays Principle",

                "explanation":

                "The Polluter Pays Principle is a major "
                "environmental governance principle."
            }
        ]

    # =====================================================
    # SCIENCE & TECHNOLOGY MCQS
    # =====================================================
    elif category == "Science & Technology":

        return [

            {
                "question":

                f"The issue related to '{title}' is important because of:",

                "options": [

                    "Technological innovation",
                    "Forest depletion",
                    "Ancient sculpture",
                    "Agrarian feudalism"
                ],

                "answer":
                "Technological innovation",

                "explanation":

                "The topic relates to technological advancement, "
                "innovation, digital transformation, "
                "and strategic technology."
            },

            {
                "question":

                "Which of the following is an "
                "emerging technology?",

                "options": [

                    "Artificial Intelligence",
                    "Bullock cart transport",
                    "Stone inscriptions",
                    "Palm leaf manuscripts"
                ],

                "answer":
                "Artificial Intelligence",

                "explanation":

                "Artificial Intelligence is a major "
                "emerging technology globally."
            }
        ]

    # =====================================================
    # SOCIAL ISSUES MCQS
    # =====================================================
    elif category == "Social Issues":

        return [

            {
                "question":

                f"The issue regarding '{title}' is important mainly due to:",

                "options": [

                    "Inclusive development concerns",
                    "Volcanic eruption patterns",
                    "Forest extraction",
                    "Oceanic salinity"
                ],

                "answer":
                "Inclusive development concerns",

                "explanation":

                "The issue is associated with social justice, "
                "welfare governance, and inclusive development."
            },

            {
                "question":

                "Which of the following contributes "
                "to human development?",

                "options": [

                    "Education and healthcare",
                    "Political instability",
                    "Trade isolation",
                    "Environmental degradation"
                ],

                "answer":
                "Education and healthcare",

                "explanation":

                "Education and healthcare are major indicators "
                "of human development."
            }
        ]

    # =====================================================
    # DEFAULT GENERAL STUDIES MCQS
    # =====================================================
    return [

        {
            "question":

            f"'{title}' is important for which UPSC stage?",

            "options": [

                "Prelims and Mains",
                "Interview only",
                "Optional only",
                "Not important"
            ],

            "answer":
            "Prelims and Mains",

            "explanation":

            "Important current affairs topics are relevant "
            "for both UPSC Prelims and Mains."
        },

        {
            "question":

            "Current affairs are important because they:",

            "options": [

                "Link static and dynamic syllabus",
                "Are unrelated to UPSC",
                "Replace NCERTs completely",
                "Focus only on entertainment"
            ],

            "answer":
            "Link static and dynamic syllabus",

            "explanation":

            "Current affairs connect static concepts "
            "with contemporary developments."
        }
    ]


# =========================================================
# GENERATE RANDOM DIFFICULTY
# =========================================================
def generate_difficulty():

    difficulties = [

        "Easy",
        "Moderate",
        "Advanced"
    ]

    return random.choice(
        difficulties
    )


# =========================================================
# GENERATE UPSC EXPLANATION
# =========================================================
def generate_explanation(category):

    explanations = {

        "Polity":
        "The topic is linked with governance, constitutional provisions, and democratic accountability.",

        "Economy":
        "The issue is connected with economic growth, fiscal management, and development policies.",

        "International Relations":
        "The issue reflects geopolitical developments and strategic interests of India.",

        "Environment":
        "The topic concerns sustainability, biodiversity, and environmental governance.",

        "Science & Technology":
        "The issue is related to innovation, emerging technologies, and digital transformation.",

        "Social Issues":
        "The issue highlights inclusive development, welfare governance, and social justice."
    }

    return explanations.get(

        category,

        "The issue has multidimensional relevance for UPSC preparation."
    )