import json
from ncert_quiz import ncert_quiz

with open("ncert_quiz_data.json", "w", encoding="utf-8") as file:
    json.dump(
        ncert_quiz,
        file,
        indent=4,
        ensure_ascii=False
    )

print("Quiz data exported successfully")