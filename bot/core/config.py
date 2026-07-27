from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BOT_TOKEN: str
    DOWNLOADS_DIR: Path = Path("downloads")
    MAX_FILE_SIZE_MB: int = 50
    # Optional: folder containing ffmpeg.exe/ffprobe.exe, for when ffmpeg
    # isn't on PATH (e.g. just extracted, not installed system-wide).
    FFMPEG_LOCATION: Optional[Path] = None

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


settings = Settings()
settings.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
