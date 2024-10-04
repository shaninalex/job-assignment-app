from sqlalchemy.ext.asyncio import AsyncSession

from pkg.models import Company
from pkg.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session: AsyncSession):
        super().__init__(Company, session)
