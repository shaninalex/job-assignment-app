from pkg.models import CompanyManager
from pkg.repositories.base import BaseRepository


class CompanyManagerRepository(BaseRepository[CompanyManager]):
    def __init__(self):
        super().__init__(CompanyManager)
