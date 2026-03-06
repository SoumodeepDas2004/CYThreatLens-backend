import time
from fastapi import APIRouter
from app.services.news_collector import fetch_news_events, news_cache

router = APIRouter(prefix="/intel")

CACHE_TTL = 600  # 10 minutes


@router.get("/events")
def get_intel_events():

    now = time.time()

    if now - news_cache["last_update"] > CACHE_TTL:

        events = fetch_news_events()

        news_cache["events"] = events
        news_cache["last_update"] = now

    return news_cache["events"]