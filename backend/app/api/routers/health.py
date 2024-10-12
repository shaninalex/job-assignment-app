from fastapi import APIRouter

from app.config import settings


router = APIRouter(
    tags=["health"]
)


@router.get("/_health")
async def health():
    return {"status": "ok", "version": settings.version}
