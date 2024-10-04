from sqlalchemy.ext.asyncio import AsyncSession

from pkg.models import User
from pkg.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
