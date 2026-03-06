from telethon import TelegramClient
import os
import time

api_id = int(os.getenv("TELE_CLND_ID"))
api_hash = os.getenv("TELE_HASH")

channels = [
    "osintdefender",
    "cybersecuritynews",
    "vxunderground"
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

        for channel in channels:

            async for message in client.iter_messages(channel, limit=10):

                if message.text:
                    print("collecting new data from telegram")
                    results.append({
                        "channel": channel,
                        "text": message.text,
                        "date": str(message.date)
                    })

    telegram_cache["data"] = results
    telegram_cache["last_update"] = now

    return results