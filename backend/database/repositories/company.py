from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Company


async def get_company(session: AsyncSession, **kwargs) -> Optional[Company]: 
    stmt = select(Company).options(
        selectinload(Company.managers),
    )

    if len(kwargs) == 0:
        return None

    if "id" in kwargs:
        stmt = stmt.where(Company.id == kwargs["id"])

    result = await session.scalars(stmt)
    company = result.one_or_none()
    return company
