import asyncio
import logging

from bot.core.loader import bot, dp
from bot.handlers.media_handler import router as media_router
from bot.services.downloader import FFMPEG_AVAILABLE


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not FFMPEG_AVAILABLE:
        logging.warning(
            "ffmpeg topilmadi — video+audio birlashtirish o'chirilgan, "
            "faqat tayyor (progressive) formatlar yuklanadi. "
            "Sifatni oshirish uchun ffmpeg o'rnatib, PATH ga qo'shing."
        )

    dp.include_router(media_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot to'xtatildi.")
