
from typing import List, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.routes.company.form import PositionForm
from pkg.consts import SalaryType
from pkg.models.models import Company, Position, User
from pkg.services.event_service import Exchanges, RoutingKeys


async def is_user_exists(session: AsyncSession, email: str) -> bool:
    result = await session.execute(select(User).where(User.email == email))
    test = result.scalar_one_or_none()
    return test is not None


async def is_company_exists(session: AsyncSession, name: str, email: str, website: str) -> bool:
    result = await session.execute(select(Company).where(
        (Company.name == name) | (Company.email == email) | (Company.website == website)
    ))
    test = result.scalar_one_or_none()
    return test is not None


T = TypeVar("T")
async def paginated_list(session: AsyncSession, model: Type[T], **kwargs) -> List[T]:
    stmt = select(model)
    filters = {}
    limit = None
    offset = None
    for k in kwargs.keys():
        if k == "limit":
            limit = kwargs[k]
        elif k == "offset":
            offset = kwargs[k]
        else:
            filters[k] = kwargs[k]

    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    if len(filters) != 0:
        for key, value in filters.items():
            stmt = stmt.where(getattr(model, key) == value)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_new_position(session: AsyncSession, payload: PositionForm) -> Position:
    position = Position(
        title=payload.title,
        description=payload.description,
        responsibilities=payload.responsibilities,
        requirements=payload.requirements,
        interview_stages=payload.interview_stages,
        offer=payload.offer,
        price_range=payload.price_range,
        remote=payload.remote,
        salary=SalaryType(payload.salary),
        hours=payload.hours,
        travel=payload.travel,
        status=payload.status,
        company_id=payload.company_id,
    )
    session.add(position)
    await session.flush()
    await session.refresh(position)
    if not position:
        raise Exception("unable to create position")
    return position