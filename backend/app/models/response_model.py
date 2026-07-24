# =========================================================
# 📁 FILE: core/models/response_model.py
# FINAL API RESPONSE FORMAT
# =========================================================

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CurrentAffairsResponse:

    title: str
    category: str
    importance: str

    quick_summary: Any
    background: str
    prelims_focus: List[str]
    mains_question: str

    tags: List[str]
    pyq_links: List[str]
    mcqs: List[Dict]
