from __future__ import annotations

import logging
import re

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from bot.core.config import settings
from bot.services.downloader import (
    DownloadError,
    FileTooLargeError,
    MediaType,
    PrivateContentError,
    UnsupportedLinkError,
    detect_platform,
    download_media,
)

router = Router(name="media")
logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(r"https?://\S+")

WELCOME_TEXT = (
    "\U0001F44B Salom!\n\n"
    "Menga YouTube, Instagram yoki Pinterest havolasini yuboring — "
    "men videoni yoki rasmni yuklab, shu yerga joylab beraman."
)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT)


@router.message(F.text.regexp(URL_PATTERN))
async def handle_media_link(message: Message) -> None:
    match = URL_PATTERN.search(message.text or "")
    if not match:
        return

    url = match.group(0)
    if detect_platform(url) is None:
        await message.answer(
            "❌ Bu havolani aniqlay olmadim. Iltimos, YouTube, Instagram "
            "yoki Pinterest havolasini yuboring."
        )
        return

    status_message = await message.answer("⏳ Yuklanmoqda...")

    try:
        result = await download_media(url)
    except UnsupportedLinkError:
        await status_message.edit_text(
            "❌ Ushbu havola qo'llab-quvvatlanmaydi. Faqat YouTube, "
            "Instagram yoki Pinterest havolalarini yuborishingiz mumkin."
        )
        return
    except PrivateContentError:
        await status_message.edit_text(
            "\U0001F512 Bu kontentni yuklab bo'lmadi — u yopiq (private) "
            "profilga tegishli bo'lishi mumkin."
        )
        return
    except FileTooLargeError:
        await status_message.edit_text(
            f"⚠️ Fayl hajmi {settings.MAX_FILE_SIZE_MB}MB dan katta "
            "bo'lgani uchun yubora olmayman."
        )
        return
    except DownloadError:
        logger.exception("Download failed for url=%s", url)
        await status_message.edit_text(
            "❌ Havoladan yuklab bo'lmadi. Havola to'g'ri va ochiq "
            "ekanligini tekshirib, qaytadan urinib ko'ring."
        )
        return
    except Exception:
        logger.exception("Unexpected error while processing url=%s", url)
        await status_message.edit_text(
            "❌ Kutilmagan xatolik yuz berdi. Birozdan so'ng qaytadan "
            "urinib ko'ring."
        )
        return

    try:
        caption = result.title[:1024] if result.title else None
        media_file = FSInputFile(result.file_path)

        if result.media_type is MediaType.PHOTO:
            await message.answer_photo(media_file, caption=caption)
        else:
            await message.answer_video(
                media_file, caption=caption, supports_streaming=True
            )
    except Exception:
        logger.exception("Failed to send media for url=%s", url)
        await status_message.edit_text("❌ Faylni yuborishda xatolik yuz berdi.")
        return
    finally:
        result.file_path.unlink(missing_ok=True)

    await status_message.delete()
