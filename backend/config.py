from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite://db.sqlite3"
    REDIS_URL: str = "redis://localhost:6379/0"

    DASHSCOPE_API_KEY: str = ""
    DASHSCOPE_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1"
    DASHSCOPE_MODEL: str = "qwen3.5-omni-plus"
    DASHSCOPE_TIMEOUT_SECONDS: int = 180

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMP_DIR: Path = BASE_DIR / "temp"
    STATIC_DIR: Path = BASE_DIR / "static"
    SCREENSHOTS_DIR: Path = STATIC_DIR / "screenshots"

    FFMPEG_PATH: str = "ffmpeg"
    YTDLP_PATH: str = ".venv/bin/yt-dlp"
    YTDLP_COOKIES_FILE: str | None = None
    YTDLP_COOKIES_FROM_BROWSER: str | None = None
    VIDEO_WIDTH: int = 1280
    VIDEO_HEIGHT: int = 720
    VIDEO_FPS: int = 30
    VIDEO_CODEC: str = "libx264"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["backend.models"],
            "default_connection": "default",
        }
    },
}
