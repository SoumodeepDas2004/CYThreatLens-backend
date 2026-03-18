import time
from fastapi import APIRouter
from app.services.news_collector import fetch_news_events,fetch_saved_news
from app.services.telegram_collector import fetch_telegram_savedmessages

router = APIRouter(prefix="/intel", tags=["Intel Map"])

CACHE_TTL = 600

cache = {
    "events": [],
    "last_update": 0
}
def is_valid_event(event):
    if not event:
        return False

    if not event.get("latitude") or not event.get("longitude"):
        return False

    if event["latitude"] == 0 or event["longitude"] == 0:
        return False

    # avoid garbage countries
    if event.get("country") in ["unk", None]:
        return False

    return True

@router.get("/events")
async def get_intel_events():

    now = time.time()

    if now - cache["last_update"] < CACHE_TTL:
        return cache["events"]

    # news_events = fetch_news_events()
    news_events=fetch_saved_news()
    telegram_events = await fetch_telegram_savedmessages()

    events = []

    for e in news_events + telegram_events:
        events.append(e)

    cache["events"] = events
    cache["last_update"] = now

    return events