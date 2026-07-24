# =========================================================
# 📁 FILE: core/models/news_model.py
# NEWS DATA MODEL
# =========================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class NewsModel:

    title: str
    description: str
    source: str
    link: str

    published_at: Optional[str] = None
    fetched_at: Optional[str] = None
