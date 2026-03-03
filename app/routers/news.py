from fastapi import APIRouter
import requests
import os

router = APIRouter(prefix="/news", tags=["News"])

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
@router.get("/global")
def get_global_news():
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=war OR military OR army OR conflict OR defense OR missile OR strike OR invasion OR geopolitics OR sanctions OR intelligence"
        f"&language=en&sortBy=publishedAt&pageSize=20&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    def detect_country(title):
        title_lower = title.lower()

        if "israel" in title_lower:
            return "Israel"
        if "russia" in title_lower:
            return "Russia"
        if "china" in title_lower:
            return "China"
        if "india" in title_lower:
            return "India"
        if "ukraine" in title_lower:
            return "Ukraine"
        if "france" in title_lower:
            return "France"
        if "us" in title_lower or "america" in title_lower:
            return "USA"
        return None

    articles = []

    for article in data.get("articles", []):
        country = detect_country(article["title"])

        articles.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "image": article["urlToImage"],
            "country": country
        })

    return articles
@router.get("/tech")
def get_tech_news():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&category=technology&pageSize=10&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = [
        {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "image": article["urlToImage"],
            "publishedAt": article["publishedAt"]
        }
        for article in data.get("articles", [])
    ]

    return articles
