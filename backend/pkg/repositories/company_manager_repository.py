from sqlalchemy.ext.asyncio import AsyncSession

from pkg.models import CompanyManager
from pkg.repositories.base import BaseRepository


class CompanyManagerRepository(BaseRepository[CompanyManager]):
    def __init__(self, session: AsyncSession):
        super().__init__(CompanyManager, session)
