import os
import logging
import sys
from dataclasses import dataclass


DEBUG = bool(int(os.getenv("DEBUG", "0")))


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
    RABBIT_URL: str
    APP_SECRET: str


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
