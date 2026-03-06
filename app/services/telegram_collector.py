from telethon import TelegramClient
import os
import time
from app.services.event_extractor import extract_event

api_id = int(os.getenv("TELE_CLND_ID"))
api_hash = os.getenv("TELE_HASH")

channels = [
    "Global_OSINT44",
    "intelslava","osintdefender",
    "CIG_telegram","geopolitics_prime",
    "cybersecuritynews","ctinow",
    
]

CACHE_TTL = 600  # 10 minutes

telegram_cache = {
    "data": [],
    "last_update": 0
}


async def fetch_telegram_messages():

    now = time.time()

    # Return cached data if within TTL
    if now - telegram_cache["last_update"] < CACHE_TTL:
        return telegram_cache["data"]

    results = []

    async with TelegramClient(
        "cythreatlens_session",
        api_id,
        api_hash
    ) as client:

        # Loop through each channel
        for channel in channels:

            async for message in client.iter_messages(channel, limit=5):

                if message.text:
                    #print("RAW MESSAGE:", message.text)
                    # print("collecting new data from telegram")
                    event = extract_event({
                        "title": message.text,
                        "source": channel,
                        "date": message.date.isoformat()
                    })
                    # print("Collected returning data")
                    if event:
                        results.append(event)

    telegram_cache["data"] = results
    telegram_cache["last_update"] = now
    print("Collected returning data")
    return results