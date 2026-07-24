from datetime import date
from app.services.article_storage import save_if_not_exists

article = {
    "title": "Iran-US Strait of Hormuz Agreement",
    "summary": "Important geopolitical development.",
    "category": "International Relations",
    "source": "Reuters",
    "importance_score": 85,
    "upsc_score": 90,
    "article_date": date.today()
}

save_if_not_exists(article)

print("✅ Test Complete")