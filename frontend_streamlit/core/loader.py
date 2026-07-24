# ==============================
# 📁 FILE: core_subjects/loader.py
# ==============================

import os
import importlib.util


# ==============================
# 📂 BASE PATH
# ==============================
BASE_PATH = os.path.join(
    "data",
    "core_subjects"
)


# ==============================
# 🧹 CLEAN NAME
# ==============================
def clean_name(name):

    return (
        name.replace(".py", "")
        .replace("_", " ")
        .title()
    )


# ==============================
# 📥 LOAD PYTHON MODULE
# ==============================
def load_module(file_path):

    try:

        module_name = os.path.basename(file_path)

        spec = importlib.util.spec_from_file_location(
            module_name,
            file_path
        )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        return module

    except Exception as e:

        print(f"❌ Error loading module: {file_path}")
        print(e)

        return None


# ==============================
# 📘 LOAD SUBJECTS
# ==============================
def load_subjects():

    subjects = {}

    # ==============================
    # ❌ PATH CHECK
    # ==============================
    if not os.path.exists(BASE_PATH):

        print("❌ BASE PATH NOT FOUND")
        print(BASE_PATH)

        return subjects

    # ==============================
    # 📚 SUBJECT LOOP
    # ==============================
    for subject in sorted(os.listdir(BASE_PATH)):

        # Ignore cache/system
        if (
            subject.startswith("__")
            or subject.startswith(".")
        ):
            continue

        subject_path = os.path.join(
            BASE_PATH,
            subject
        )

        if not os.path.isdir(subject_path):
            continue

        subjects[subject] = {}

        items = sorted(os.listdir(subject_path))

        # ==============================
        # 📂 DETECT STRUCTURE
        # ==============================
        py_files = []
        folders = []

        for item in items:

            full_path = os.path.join(
                subject_path,
                item
            )

            if os.path.isfile(full_path) and item.endswith(".py"):

                if not item.startswith("__"):
                    py_files.append(item)

            elif os.path.isdir(full_path):

                if not item.startswith("__"):
                    folders.append(item)

        # ==================================================
        # CASE 1:
        # SUBJECT → DIRECT CHAPTERS
        #
        # polity/
        #   parliament.py
        #   judiciary.py
        # ==================================================
        if py_files:

            subjects[subject]["General"] = {}

            for file in py_files:

                file_path = os.path.join(
                    subject_path,
                    file
                )

                module = load_module(file_path)

                if not module:
                    continue

                if hasattr(module, "TOPICS"):

                    chapter_name = clean_name(file)

                    subjects[subject]["General"][chapter_name] = {
                        "topics": module.TOPICS
                    }

        # ==================================================
        # CASE 2:
        # SUBJECT → SUB SUBJECTS → CHAPTERS
        #
        # geography/
        #   physical/
        #       geomorphology.py
        # ==================================================
        for folder in folders:

            folder_path = os.path.join(
                subject_path,
                folder
            )

            subjects[subject][clean_name(folder)] = {}

            files = sorted(os.listdir(folder_path))

            for file in files:

                if (
                    file.startswith("__")
                    or not file.endswith(".py")
                ):
                    continue

                file_path = os.path.join(
                    folder_path,
                    file
                )

                module = load_module(file_path)

                if not module:
                    continue

                if hasattr(module, "TOPICS"):

                    chapter_name = clean_name(file)

                    subjects[subject][clean_name(folder)][chapter_name] = {
                        "topics": module.TOPICS
                    }

    return subjects


# ==============================
# 📖 LOAD SINGLE SUBJECT
# ==============================
def load_subject(subject_name):

    subjects = load_subjects()

    return subjects.get(subject_name, {})


# ==============================
# 📄 GET CHAPTERS
# ==============================
def get_chapters(subject, sub_subject=None):

    subjects = load_subjects()

    if subject not in subjects:
        return {}

    if sub_subject:

        return subjects[subject].get(
            sub_subject,
            {}
        )

    return subjects[subject]


# ==============================
# 📘 GET TOPICS
# ==============================
def get_topics(subject, sub_subject, chapter):

    subjects = load_subjects()

    try:

        return (
            subjects[subject][sub_subject][chapter]
            .get("topics", [])
        )

    except:

        return []


# ==============================
# 🧪 DEBUG LOADER
# ==============================
def debug_loader():

    data = load_subjects()

    print("\n========== SUBJECTS ==========\n")

    for subject in data:

        print(f"\n📘 SUBJECT: {subject}")

        for sub in data[subject]:

            print(f"   📂 SUB: {sub}")

            for chapter in data[subject][sub]:

                print(f"      📄 {chapter}")

                topics = (
                    data[subject][sub][chapter]
                    .get("topics", [])
                )

                print(f"         Topics: {len(topics)}")