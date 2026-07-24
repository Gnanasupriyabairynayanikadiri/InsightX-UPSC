# =========================================================
# 📁 FILE: core/models/mcq_model.py
# MCQ DATA MODEL
# =========================================================

from dataclasses import dataclass
from typing import List


@dataclass
class MCQModel:

    question: str
    options: List[str]
    answer: str
