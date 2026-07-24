from sqlalchemy import text
from app.database.db import engine


def generate_monthly_magazine(month_year):

    query = text("""
        SELECT
            article_date,
            title,
            category,
            summary,
            upsc_score
        FROM current_affairs_articles
        WHERE FORMAT(article_date,'yyyy-MM') = :month_year
        ORDER BY article_date
    """)

    with engine.connect() as conn:
        articles = conn.execute(
            query,
            {"month_year": month_year}
        ).mappings().all()

    if len(articles) == 0:
        print("No Articles Found")
        return

    content = f"# UPSC Monthly Current Affairs Magazine ({month_year})\n\n"

    categories = {}

    for article in articles:

        category = article["category"]

        if category not in categories:
            categories[category] = []

        categories[category].append(article)

    for category, items in categories.items():

        content += f"## {category}\n\n"

        for item in items:

            content += f"""
### {item['title']}

**Date:** {item['article_date']}

**Summary:**
{item['summary']}

**UPSC Score:** {item['upsc_score']}

---

"""

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO monthly_magazines
                (
                    month_year,
                    total_articles,
                    magazine_content
                )
                VALUES
                (
                    :month_year,
                    :total_articles,
                    :magazine_content
                )
            """),
            {
                "month_year": month_year,
                "total_articles": len(articles),
                "magazine_content": content
            }
        )

    print("=" * 60)
    print("MAGAZINE GENERATED SUCCESSFULLY")
    print("Month :", month_year)
    print("Articles :", len(articles))
    print("=" * 60)


if __name__ == "__main__":

    generate_monthly_magazine("2026-06")