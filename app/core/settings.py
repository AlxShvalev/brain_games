import os
from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = os.path.join(BASE_DIR / ".env")


class Settings(BaseSettings):
    """Application settings class."""
    # Hosting settings
    host: str
    ip_port: int

    # Database settings
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str

    # Application settings
    title: str = "Brain Games"
    debug: bool = False
    reload: bool = False
    root_path: str = ""
    media_dir: str = "media"

    @property
    def database_url(self) -> str:
        """Get db connection url."""
        return "sqlite:///foo.db"
        # return (
        #     "postgresql+asyncpg://"
        #     f"{self.db_user}:{self.db_password}"
        #     f"@{self.db_host}:{self.db_port}/{self.db_name}"
        # )

    class Config:
        env_file = ENV_FILE


settings = Settings()
