import time
from fastapi import APIRouter
from app.services.news_collector import fetch_news_events
from app.services.telegram_collector import fetch_telegram_messages

router = APIRouter(prefix="/intel", tags=["Intel Map"])

CACHE_TTL = 600

cache = {
    "events": [],
    "last_update": 0
}

@router.get("/events")
async def get_intel_events():

    now = time.time()

    if now - cache["last_update"] < CACHE_TTL:
        return cache["events"]

    news_events = fetch_news_events()
    telegram_events = await fetch_telegram_messages()

    events = news_events + telegram_events

    cache["events"] = events
    cache["last_update"] = now

    return events