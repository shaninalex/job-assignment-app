from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter(tags=["health"])


class APIHealth(BaseModel):
    status: str
    version: str


@router.get("/_health")
async def health() -> APIHealth:
    return APIHealth(status="ok", version=settings.version)
