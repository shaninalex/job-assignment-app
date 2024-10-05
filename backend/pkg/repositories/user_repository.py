from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pkg.models import User
from pkg.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user(self, **kwargs):
        stmt = select(User).options(selectinload(User.manager))

        if "id" in kwargs:
            stmt = stmt.where(User.id == kwargs["id"])

        if "email" in kwargs:
            stmt = stmt.where(User.email == kwargs["email"])

        if "active" in kwargs:
            stmt = stmt.where(User.active == kwargs["active"])

        if "status" in kwargs:
            stmt = stmt.where(User.status == kwargs["status"])

        result = await self.session.scalars(stmt)
        user = result.one_or_none()
        return user