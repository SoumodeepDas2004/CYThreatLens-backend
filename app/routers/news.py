from fastapi import APIRouter
import requests
import os
import feedparser
import time

router = APIRouter(prefix="/news", tags=["News"])

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# cache system to avoid API overuse
cache = {
    "global": [],
    "tech": [],
    "rss": [],
    "last_update": 0
}

CACHE_TTL = 600  # 10 minutes


# -------------------------------
# COUNTRY DETECTION
# -------------------------------
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
    if "iran" in title_lower:
        return "Iran"
    if "usa" in title_lower or "america" in title_lower:
        return "USA"

    return None


# -------------------------------
# GLOBAL CONFLICT NEWS
# -------------------------------
@router.get("/global")
def get_global_news():

    now = time.time()

    if now - cache["last_update"] < CACHE_TTL:
        return cache["global"]

    url = (
        "https://newsapi.org/v2/everything?"
        "q=war OR military OR army OR conflict OR defense OR missile OR strike OR invasion OR geopolitics OR sanctions OR intelligence"
        "&language=en&sortBy=publishedAt&pageSize=20"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

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

    cache["global"] = articles
    cache["last_update"] = now

    return articles


# -------------------------------
# TECH / CYBER NEWS
# -------------------------------
@router.get("/tech")
def get_tech_news():

    now = time.time()

    if cache["tech"] and now - cache["last_update"] < CACHE_TTL:
        return cache["tech"]

    url = (
        "https://newsapi.org/v2/top-headlines?"
        "language=en&category=technology&pageSize=10"
        f"&apiKey={NEWS_API_KEY}"
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

    cache["tech"] = articles
    return articles


# -------------------------------
# RSS CYBER NEWS
# -------------------------------
RSS_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml"
]


@router.get("/rss")
def get_rss_news():

    news = []

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:

            news.append({
                "title": entry.title,
                "url": entry.link,
                "source": feed.feed.title
            })

    return news