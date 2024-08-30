from typing import List, Optional

from sqlalchemy import Sequence, select
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
        company_id=payload.company_id
    )
    session.add(position)
    await session.commit()

    return position


async def get_position(session: AsyncSession, **kwargs) -> Optional[Position]: 
    stmt = select(Position).options(
        # selectinload(<relations>),
    )

    if len(kwargs) == 0:
        return None

    if "id" in kwargs:
        stmt = stmt.where(Position.id == kwargs["id"])

    result = await session.scalars(stmt)
    position = result.one_or_none()
    return position


async def get_positions(session: AsyncSession, **kwargs) -> List[Position]: 
    stmt = select(Position).options(
        # selectinload(<relations>),
    )

    if len(kwargs) == 0:
        return []

    if "company_id" in kwargs:
        stmt = stmt.where(Position.company_id == kwargs["company_id"])

    result = await session.scalars(stmt)
    position = result.all()

    return list(position)

