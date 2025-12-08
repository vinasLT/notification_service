from aiogram import Bot

from config import settings
from core.logger import logger


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


async def send_telegram(message: str) -> None:
    logger.info("Sending telegram notification", extra={"recipients": settings.ADMINS_TG_ID, "message": message})

    try:
        for admin_id in settings.ADMINS_TG_ID:
            await bot.send_message(chat_id=admin_id, text=message)
        logger.debug("Telegram notification sent", extra={"recipients": settings.ADMINS_TG_ID})
    except Exception as exc:
        logger.error("Error sending telegram notification", extra={"recipients": settings.ADMINS_TG_ID, "error": str(exc)})
