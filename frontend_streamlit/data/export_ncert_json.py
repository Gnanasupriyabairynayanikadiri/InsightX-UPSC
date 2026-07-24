import json
from ncert_lessons import ncert_lessons

with open("ncert_data.json", "w", encoding="utf-8") as file:
    json.dump(
        ncert_lessons,
        file,
        indent=4,
        ensure_ascii=False
    )

print("✅ NCERT data exported successfully!")