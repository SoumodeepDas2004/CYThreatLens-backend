from fastapi import APIRouter
import asyncio
from app.services.telegram_collector import fetch_telegram_messages

router = APIRouter(prefix="/telegram", tags=["Telegram Intel"])

@router.get("/intel")
async def get_telegram_intel():

    data = await fetch_telegram_messages()

    return data