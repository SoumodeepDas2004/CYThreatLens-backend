import feedparser
from app.services.event_extractor import extract_event

RSS_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml"
]

news_cache = {
    "events": [],
    "last_update": 0
}


def fetch_news_events():
    events = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            article = {
                "title": entry.title,
                "source": url
            }

            event = extract_event(article)

            if event:
                events.append(event)

    return events