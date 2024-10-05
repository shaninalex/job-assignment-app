from pkg.models import Company
from pkg.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)
