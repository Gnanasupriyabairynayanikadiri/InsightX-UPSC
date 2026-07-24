import os


# =========================================
# APP INFO
# =========================================
APP_NAME = "InsightX"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Smart UPSC Learning Platform"


# =========================================
# BASE PATHS
# =========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STORAGE_DIR = os.path.join(BASE_DIR, "storage")
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# =========================================
# FILE PATHS
# =========================================
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")
XP_FILE = os.path.join(STORAGE_DIR, "xp.json")
PROGRESS_FILE = os.path.join(STORAGE_DIR, "progress.json")
COMMUNITY_FILE = os.path.join(STORAGE_DIR, "community.json")
LEADERBOARD_FILE = os.path.join(STORAGE_DIR, "leaderboard.json")


# =========================================
# XP SYSTEM
# =========================================
XP_PER_QUIZ = 5
XP_PER_CORRECT = 10
XP_PER_ANSWER = 10
XP_PER_POST = 5

LEVEL_XP = 100


# =========================================
# ANSWER WRITING SETTINGS
# =========================================
MIN_WORDS = 80
MAX_WORDS = 300
MAX_SCORE = 10


# =========================================
# SUBJECT STRUCTURE
# =========================================
SUBJECTS = ["GS1", "GS2", "GS3", "GS4"]


LEVELS = ["Basic", "Moderate", "Advanced"]


# =========================================
# USER ROLES
# =========================================
ROLE_USER = "user"
ROLE_ADMIN = "admin"


# =========================================
# QUESTION BANK (FIXED CORE)
# =========================================
QUESTION_BANK = {
    "GS1": {
        "Art & Culture": {
            "Architecture": {

                "Basic": [
                    {
                        "question": "Discuss the main features of Harappan architecture with suitable examples.",
                        "marks": 10,
                        "topic_keywords": ["harappa", "indus", "dholavira"]
                    },
                    {
                        "question": "Explain the characteristics of Mauryan architecture. Highlight the role of Ashoka.",
                        "marks": 10,
                        "topic_keywords": ["mauryan", "ashoka", "stupa", "pillar"]
                    },
                    {
                        "question": "What are the important features of Post-Mauryan architecture in India?",
                        "marks": 10,
                        "topic_keywords": ["gandhara", "kushana", "stupa"]
                    },
                    {
                        "question": "Describe the major characteristics of Gupta period temple architecture.",
                        "marks": 10,
                        "topic_keywords": ["gupta", "temple", "nagara"]
                    },
                    {
                        "question": "Write a short note on Khajuraho temples.",
                        "marks": 10,
                        "topic_keywords": ["khajuraho", "chandela", "nagara"]
                    }
                ],

                "Moderate": [
                    {
                        "question": "Compare Nagara and Dravidian temple architecture.",
                        "marks": 15,
                        "topic_keywords": ["nagara", "dravidian", "shikhara", "vimana"]
                    }
                ],

                "Advanced": [
                    {
                        "question": "Critically analyse the evolution of temple architecture in India.",
                        "marks": 15,
                        "topic_keywords": ["temple", "evolution", "india"]
                    }
                ]
            }
        }
    }
}