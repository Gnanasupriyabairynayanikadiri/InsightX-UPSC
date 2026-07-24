# =========================================================
# 📁 FILE: core/models/schemas.py
# FASTAPI REQUEST/RESPONSE SCHEMAS
# =========================================================

from pydantic import BaseModel
from typing import List, Dict, Any


class NewsResponseSchema(BaseModel):

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
