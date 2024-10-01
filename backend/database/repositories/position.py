from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from api.routes.company import PositionForm
from api.routes.company.types import PositionFormPatch
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
    stmt = select(Position).options()

    # Add filter conditions only if provided in kwargs
    if "company_id" in kwargs:
        stmt = stmt.where(Position.company_id == kwargs["company_id"])

    # Execute the query
    result = await session.scalars(stmt)
    positions = result.all()

    return list(positions)

async def update_position(session: AsyncSession, id: UUID, payload: PositionFormPatch) -> Optional[Position]:
    values: dict[str, Any] = {}
    data = payload.model_dump()
    for key in data.keys():
        if data[key] is not None:
            values[key] = data[key]
        
    if not len(values):
        return None

    stmt = update(Position).where(Position.id == id).values(**values).returning(Position.id)
    result = await session.execute(stmt)

    if not result:
        return None

    await session.commit()
    return await get_position(session, id=id)
