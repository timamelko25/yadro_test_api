import os

from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{line} | {message}"
    LOG_ROTATION: str = "10 MB"

    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_NAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_pg_url(self):
        return (
            f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"
        )


settings = Settings()  # type: ignore

PG_URL = settings.get_pg_url()


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(parent_dir, "log.txt")
logger.add(
    log_file_path,
    format=settings.FORMAT_LOG,
    level="INFO",
    rotation=settings.LOG_ROTATION,
)

