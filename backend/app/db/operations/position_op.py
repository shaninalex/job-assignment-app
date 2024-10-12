from typing import List, Optional, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.core_types import Pagination
from app.db.models import Position
from app.enums import Remote, SalaryType, WorkingHours, TravelRequired, PositionStatus
from app.exceptions.exceptions import ServiceError


class PositionNotFoundError(ServiceError):
    pass


class PartialPositionParamsPayload(BaseModel, extra="forbid"):
    company_id: Optional[UUID] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None


class PartialPositionSearchPayload(BaseModel, extra="forbid"):
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
    string_params: Optional[PartialPositionSearchPayload] = None,
    pagination: Optional[Pagination] = None,
) -> List[Position] | Sequence[Position]:
    if not params and not string_params:
        raise PositionListOptionsRequiredError()

    stmt = select(Position)
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
        for field, value in string_params.model_dump(exclude_unset=True).items():
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
    position = Position(
        title=payload.title,
        company_id=payload.company_id,
        description=payload.description,
    )

    if payload.interview_stages:
        position.interview_stages = payload.interview_stages
    if payload.responsibilities:
        position.responsibilities = payload.responsibilities
    if payload.requirements:
        position.requirements = payload.requirements
    if payload.offer:
        position.offer = payload.offer
    if payload.remote:
        position.remote = payload.remote
    if payload.salary:
        position.salary = payload.salary
    if payload.hours:
        position.hours = payload.hours
    if payload.travel:
        position.travel = payload.travel
    if payload.status:
        position.status = payload.status
    if payload.price_range:
        position.price_range = payload.price_range

    session.add(position)
    await session.flush()
    await session.refresh(position)
    return position


async def position_get_by_id(session: AsyncSession, position_id) -> Position:
    stmt = select(Position).where(Position.id == position_id)
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


async def position_update(session: AsyncSession, position_id: UUID, payload: PartialPositionUpdatePayload) -> Position:
    position = await position_get_by_id(session, position_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(position, key, value)
    await session.flush()
    return position


async def position_delete(session: AsyncSession, position_id: UUID, company_id: UUID):
    stmt = delete(Position).where((Position.id == position_id) & (Position.company_id == company_id))
    await session.execute(stmt)
    await session.flush()
