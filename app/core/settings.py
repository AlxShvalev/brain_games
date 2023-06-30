import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = os.path.join(BASE_DIR / ".env")


class Settings(BaseSettings):
    """Настройки приложения."""

    DEBUG: bool = False

    # Hosting settings
    HOST: str
    IP_PORT: int

    # Database settings
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    # Application settings
    TITLE: str = "Brain Games"
    RELOAD: bool = False
    ROOT_PATH: str = "/api/v1"
    MEDIA_DIR: str = BASE_DIR / "media"

    @property
    def database_url(self) -> str:
        """Get db connection url."""
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ENV_FILE


settings = Settings()
