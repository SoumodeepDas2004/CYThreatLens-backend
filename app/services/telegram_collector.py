from telethon import TelegramClient
import os
import time
from app.services.event_extractor import extract_event
from datetime import datetime, timedelta, timezone
import base64

# Load session (only once)
session_data = os.getenv("SESSION_DATA")

if session_data and not os.path.exists("cythreatlens_session.session"):
    with open("cythreatlens_session.session", "wb") as f:
        f.write(base64.b64decode(session_data))

api_id = int(os.getenv("TELE_CLND_ID"))
api_hash = os.getenv("TELE_HASH")

channels = [
    "Global_OSINT44",
    "intelslava","osintdefender",
    "CIG_telegram","geopolitics_prime",
    "cybersecuritynews","ctinow",
    "cyintel01"
]

CACHE_TTL = 600

telegram_cache = {
    "data": [],
    "last_update": 0
}

async def fetch_telegram_messages():

    now = time.time()

    if now - telegram_cache["last_update"] < CACHE_TTL:
        return telegram_cache["data"]

    results = []

    client = TelegramClient("cythreatlens_session", api_id, api_hash)
    await client.connect()

    for channel in channels:
        async for message in client.iter_messages(channel, limit=5):

            if message.text:
                post_url = f"https://t.me/{channel}/{message.id}"

                if message.date < datetime.now(timezone.utc) - timedelta(days=2):
                    continue

                event = extract_event({
                    "title": message.text,
                    "source": channel,
                    "url": post_url,
                    "date": message.date.isoformat()
                })

                if event:
                    results.append(event)

    await client.disconnect()

    telegram_cache["data"] = results
    telegram_cache["last_update"] = now

    return results


# async def fetch_telegram_savedmessages():
#     return telegram_cache["data"]

async def fetch_telegram_savedmessages():
    if(telegram_cache["data"]):return telegram_cache["data"]
    return []