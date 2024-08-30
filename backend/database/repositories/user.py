from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import User


async def get_user(session: AsyncSession, **kwargs) -> Optional[User]: 
    stmt = select(User).options(
        selectinload(User.manager),
    )

    if len(kwargs) == 0:
        return None

    if "id" in kwargs:
        stmt = stmt.where(User.id == kwargs["id"])

    if "email" in kwargs:
        stmt = stmt.where(User.email == kwargs["email"])

    if "active" in kwargs:
        stmt = stmt.where(User.active == kwargs["active"])

    if "status" in kwargs:
        stmt = stmt.where(User.status == kwargs["status"])

    result = await session.scalars(stmt)
    user = result.one_or_none()
    return user
