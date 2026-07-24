# =========================================================
# 📁 FILE: core/models/editorial_model.py
# UPSC EDITORIAL STRUCTURE
# =========================================================

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class EditorialModel:

    gs_paper: str
    background: str
    significance: List[str]
    mains_question: str
    answer_framework: Dict
