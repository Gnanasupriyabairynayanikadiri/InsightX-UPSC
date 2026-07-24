from app.fetchers.news_fetcher import fetch_daily_news
from app.current_affairs.generator import get_daily_current_affairs

def get_daily_ca():

    raw_news = fetch_daily_news()
    processed = get_daily_current_affairs(raw_news)

    return {
        "count": len(processed),
        "data": processed
    }
