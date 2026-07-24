# ==========================================
# 📁 FILE: core/mains_engine/question_bank/question_bank_loader.py
# ==========================================

import os
import importlib.util
import random

BASE_PATH = os.path.dirname(__file__)


# ==========================================
# LOAD MODULE SAFELY
# ==========================================
def load_module(file_path):

    try:
        module_name = os.path.basename(file_path).replace(".py", "")

        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path
        )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        return module

    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


# ==========================================
# MERGE DICTIONARIES SAFELY
# ==========================================
def merge_dict(main, new):

    if not isinstance(new, dict):
        return main

    for key, value in new.items():

        if key not in main:
            main[key] = value

        else:

            if isinstance(value, dict) and isinstance(main[key], dict):
                merge_dict(main[key], value)

            elif isinstance(value, list) and isinstance(main[key], list):
                main[key].extend(value)


# ==========================================
# BUILD QUESTION BANK
# ==========================================
def load_question_bank():

    full_bank = {}
    loaded_files = 0
    failed_files = 0

    for root, _, files in os.walk(BASE_PATH):

        for file in files:

            if (
                not file.endswith(".py")
                or file.startswith("__")
                or file == "question_bank_loader.py"
            ):
                continue

            file_path = os.path.join(root, file)

            module = load_module(file_path)

            if not module:
                failed_files += 1
                continue

            # CASE 1: QUESTION_BANK structure
            if hasattr(module, "QUESTION_BANK"):

                try:
                    merge_dict(full_bank, module.QUESTION_BANK)
                    loaded_files += 1

                except Exception as e:
                    print(f"❌ Merge error in {file_path}: {e}")
                    failed_files += 1

            # CASE 2: SIMPLE QUESTIONS LIST
            elif hasattr(module, "QUESTIONS"):

                subject = os.path.basename(root)

                if subject not in full_bank:
                    full_bank[subject] = []

                full_bank[subject].extend(module.QUESTIONS)
                loaded_files += 1

    print(f"✅ Question Bank Loaded | Files: {loaded_files} | Failed: {failed_files}")

    return full_bank


# ==========================================
# GLOBAL EXPORT (IMPORTANT FIX)
# ==========================================
QUESTION_BANK = load_question_bank()


# ==========================================
# GET RANDOM QUESTION (SAFE)
# ==========================================
def get_random_question():

    all_questions = []

    def collect(data):

        if isinstance(data, list):

            for item in data:
                if isinstance(item, dict) and "question" in item:
                    all_questions.append(item)

        elif isinstance(data, dict):

            for value in data.values():
                collect(value)

    collect(QUESTION_BANK)

    return random.choice(all_questions) if all_questions else None


# ==========================================
# DEBUG HELPER (OPTIONAL)
# ==========================================
def debug_bank():

    print("\n📊 QUESTION BANK STRUCTURE")
    print("-" * 40)

    print(f"Subjects: {len(QUESTION_BANK)}")

    for subject in QUESTION_BANK:
        print(f"✔ {subject}")