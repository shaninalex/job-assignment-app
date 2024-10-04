import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DEBUG = bool(int(os.getenv("DEBUG", "0")))
TIMEOUT = int(os.getenv("TIMEOUT", "0"))
DSN = "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
JWT_SECRET = os.getenv("JWT_SECRET")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


DATABASE_URI = DSN.format(
    DB_USERNAME=os.getenv("DB_USERNAME", "postgres_user"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=int(os.getenv("DB_PORT", "5432")),
    DB_NAME=os.getenv("DB_NAME"),
)


@dataclass
class Redis:
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


@dataclass
class Config:
    DATABASE_URI: str
    DEBUG: bool
    REDIS: Redis
    APP_PORT: int


def config() -> Config:
    return Config(
        DATABASE_URI=DATABASE_URI,
        DEBUG=DEBUG,
        APP_PORT=int(os.getenv("APP_PORT", "8080")),
        REDIS=Redis(
            REDIS_HOST=REDIS_HOST,
            REDIS_PORT=REDIS_PORT,
            REDIS_DB=REDIS_DB,
        ),
    )


CONFIG = config()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
