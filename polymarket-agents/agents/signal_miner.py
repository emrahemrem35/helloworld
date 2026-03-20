import requests
import os
from datetime import datetime, timedelta


def get_news_signals(query: str) -> list:
    """İlgili haberleri çek"""
    api_key = os.getenv("NEWS_API_KEY")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={query}&from={yesterday}&sortBy=relevancy&apiKey={api_key}"
    )
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])[:5]
        return [
            a["title"] + " — " + a["description"]
            for a in articles
            if a.get("description")
        ]
    return []
