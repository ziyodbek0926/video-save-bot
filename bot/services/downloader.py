from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import uuid4

import yt_dlp

from bot.core.config import settings

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

YOUTUBE_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)[\w-]+",
    re.IGNORECASE,
)
INSTAGRAM_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?instagram\.com/(?:reel|reels|p|tv)/[\w-]+",
    re.IGNORECASE,
)
PINTEREST_PATTERN = re.compile(
    r"(?:https?://)?(?:[\w-]+\.)?pinterest\.[a-z.]+/pin/[\w-]+|(?:https?://)?pin\.it/[\w-]+",
    re.IGNORECASE,
)


class Platform(str, Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    PINTEREST = "pinterest"


class MediaType(str, Enum):
    VIDEO = "video"
    PHOTO = "photo"


@dataclass(slots=True)
class DownloadResult:
    file_path: Path
    media_type: MediaType
    title: str
    platform: Platform


class DownloadError(Exception):
    """Base exception for all download failures."""


class UnsupportedLinkError(DownloadError):
    """Raised when the URL does not belong to a supported platform."""


class PrivateContentError(DownloadError):
    """Raised when the content is private or requires login to access."""


class FileTooLargeError(DownloadError):
    """Raised when the downloaded file exceeds the configured size limit."""

    def __init__(self, size_bytes: int) -> None:
        self.size_bytes = size_bytes
        super().__init__(f"File size {size_bytes} bytes exceeds the configured limit")


def detect_platform(url: str) -> Optional[Platform]:
    if YOUTUBE_PATTERN.search(url):
        return Platform.YOUTUBE
    if INSTAGRAM_PATTERN.search(url):
        return Platform.INSTAGRAM
    if PINTEREST_PATTERN.search(url):
        return Platform.PINTEREST
    return None


def _format_selector() -> str:
    limit = f"{settings.MAX_FILE_SIZE_MB}M"
    return (
        f"bestvideo[ext=mp4][filesize<{limit}]+bestaudio[ext=m4a][filesize<{limit}]/"
        f"best[ext=mp4][filesize<{limit}]/"
        f"bestvideo[filesize<{limit}]+bestaudio[filesize<{limit}]/"
        f"best[filesize<{limit}]/"
        "worst"
    )


def _resolve_downloaded_path(info: dict, file_id: str) -> Optional[Path]:
    for requested in info.get("requested_downloads") or []:
        filepath = requested.get("filepath")
        if filepath and Path(filepath).exists():
            return Path(filepath)

    for candidate in sorted(settings.DOWNLOADS_DIR.glob(f"{file_id}.*")):
        if candidate.is_file():
            return candidate

    return None


def _classify_error(exc: Exception) -> DownloadError:
    message = str(exc).lower()

    private_markers = (
        "login required",
        "log in",
        "private",
        "requires authentication",
        "requested content is not available",
    )
    unsupported_markers = (
        "unsupported url",
        "no video formats found",
        "unable to extract",
    )

    if any(marker in message for marker in private_markers):
        return PrivateContentError(str(exc))
    if any(marker in message for marker in unsupported_markers):
        return UnsupportedLinkError(str(exc))
    return DownloadError(str(exc))


def _download_sync(url: str, platform: Platform) -> DownloadResult:
    file_id = uuid4().hex
    outtmpl = str(settings.DOWNLOADS_DIR / f"{file_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "format": _format_selector(),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "restrictfilenames": True,
        "retries": 3,
        "socket_timeout": 20,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except yt_dlp.utils.DownloadError as exc:
        raise _classify_error(exc) from exc

    if not info:
        raise DownloadError("Media ma'lumotlarini olib bo'lmadi.")

    if "entries" in info:
        entries = [entry for entry in info["entries"] if entry]
        if not entries:
            raise DownloadError("Yuklab olish uchun kontent topilmadi.")
        info = entries[0]

    filepath = _resolve_downloaded_path(info, file_id)
    if filepath is None:
        raise DownloadError("Yuklangan fayl topilmadi.")

    size_bytes = filepath.stat().st_size
    if size_bytes > settings.max_file_size_bytes:
        filepath.unlink(missing_ok=True)
        raise FileTooLargeError(size_bytes)

    ext = (info.get("ext") or filepath.suffix.lstrip(".")).lower()
    media_type = MediaType.PHOTO if ext in IMAGE_EXTENSIONS else MediaType.VIDEO

    return DownloadResult(
        file_path=filepath,
        media_type=media_type,
        title=(info.get("title") or "").strip(),
        platform=platform,
    )


async def download_media(url: str) -> DownloadResult:
    platform = detect_platform(url)
    if platform is None:
        raise UnsupportedLinkError(url)

    return await asyncio.to_thread(_download_sync, url, platform)
