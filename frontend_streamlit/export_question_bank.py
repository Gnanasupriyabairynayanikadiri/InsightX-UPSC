# export_question_bank.py

from core.mains_engine.question_bank.question_bank_loader import QUESTION_BANK
import json

with open("question_bank.json", "w", encoding="utf-8") as f:
    json.dump(
        QUESTION_BANK,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Export completed")