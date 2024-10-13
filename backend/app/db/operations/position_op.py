from typing import List, Optional, Sequence, Dict
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.core_types import Pagination
from app.db.models import Position
from app.enums import Remote, SalaryType, WorkingHours, TravelRequired, PositionStatus
from app.exceptions.exceptions import ServiceError


class PositionNotFoundError(ServiceError):
    pass


class PartialPositionParamsPayload(BaseModel):
    company_id: Optional[UUID] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None


class PartialPositionSearchPayload(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    interview_stages: Optional[str] = None
    offer: Optional[str] = None
    price_range: Optional[str] = None


class PositionListOptionsRequiredError(ServiceError):
    pass


async def positions_list(
    session: AsyncSession,
    params: Optional[PartialPositionParamsPayload] = None,
    string_params: Optional[Dict] = None,
    pagination: Optional[Pagination] = None,
) -> List[Position] | Sequence[Position]:
    # if not params and not string_params or not pagination:
    #     raise PositionListOptionsRequiredError(message="No params provided in positions list")

    stmt = select(Position).options(selectinload(Position.company))
    filters = []

    if params:
        # search params
        if params.company_id:
            filters.append(Position.company_id == params.company_id)
        if params.remote:
            filters.append(Position.remote == params.remote)
        if params.salary:
            filters.append(Position.salary == params.salary)
        if params.hours:
            filters.append(Position.hours == params.hours)
        if params.travel:
            filters.append(Position.travel == params.travel)
        if params.status:
            filters.append(Position.status == params.status)

    if string_params:
        # search values
        for field, value in string_params.items():
            filters.append(getattr(Position, field).ilike(f"%{value}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    if pagination:
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)

        if pagination.offset:
            stmt = stmt.limit(pagination.offset)

    # TODO: sorting

    result = await session.execute(stmt)
    positions = result.scalars().all()
    return positions


class PositionCreatePayload(BaseModel, extra="forbid"):
    title: str
    company_id: UUID
    description: str

    interview_stages: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    offer: Optional[str] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None
    price_range: Optional[str] = None


async def position_create(session: AsyncSession, payload: PositionCreatePayload) -> Position:
    position = Position(**payload.model_dump(exclude_unset=True))
    session.add(position)
    await session.flush()
    await session.refresh(position)
    return position


async def position_get_by_id(session: AsyncSession, position_id, **kwargs) -> Position:
    stmt = select(Position).where(Position.id == position_id)

    for key, value in kwargs.items():
        if getattr(Position, key):
            stmt = stmt.where(getattr(Position, key) == value)

    result = await session.execute(stmt)
    position = result.scalar_one_or_none()
    if position is None:
        raise PositionNotFoundError(f"Position with ID {position_id} not found.")
    return position


class PartialPositionUpdatePayload(BaseModel, extra="forbid"):
    title: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    interview_stages: Optional[str] = None
    offer: Optional[str] = None
    price_range: Optional[str] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None


async def position_update(
    session: AsyncSession, position_id: UUID, payload: PartialPositionUpdatePayload, **kwargs
) -> Position:
    position = await position_get_by_id(session, position_id, **kwargs)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(position, key, value)
    await session.flush()
    return position


async def position_delete(session: AsyncSession, position_id: UUID, company_id: UUID):
    await position_get_by_id(session, position_id, **{"company_id": company_id})
    stmt = delete(Position).where((Position.id == position_id) & (Position.company_id == company_id))
    await session.execute(stmt)
    await session.flush()
