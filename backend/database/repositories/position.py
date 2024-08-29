from typing import Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from api.routes.company import PositionForm
from database import (
    Position
)


async def create_position(session: AsyncSession, payload: PositionForm) -> Optional[Position]:
    position = Position(
        title=payload.title,
        description=payload.description,
        responsibilities=payload.responsibilities,
        requirements=payload.requirements,
        interview_stages=payload.interview_stages,
        offer=payload.offer,
        price_range=payload.price_range,
        remote=payload.remote,
        salary=payload.salary,
        hours=payload.hours,
        travel=payload.travel,
        status=payload.status,
    )
    session.add(position)
    await session.commit()
    return position