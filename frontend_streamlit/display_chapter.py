import time

def display_chapter(subject, class_name, chapter_num):
    chapter = ncert_lessons[subject][class_name]["Chapters"][chapter_num]

    print("\n📘", chapter["title"])
    print("-" * 50)

    for section in chapter["notes"]:
        print(f"\n🔹 {section['heading']}")
        for point in section["points"]:
            print(f"   • {point}")
            time.sleep(0.4)   # 🔥 smooth learning feel

    # 🔥 Next / Back option
    choice = input("\n1. Next Chapter  2. Back: ")

    if choice == "1":
        next_ch = chapter_num + 1
        if next_ch in ncert_lessons[subject][class_name]["Chapters"]:
            display_chapter(subject, class_name, next_ch)
        else:
            print("📌 No more chapters!")