from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pkg.consts import ConfirmStatusCode
from pkg.models import ConfirmCode
from pkg.repositories.base import BaseRepository


class ConfirmCodeRepository(BaseRepository[ConfirmCode]):
    """
    ConfirmCodeRepository(session)

    Repository class for handling operations related to ConfirmCode entity.

    Parameters
    ----------
    session : AsyncSession
        The SQLAlchemy asynchronous session to be used for database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(ConfirmCode, session)

    async def get_code(self, code_id: str, code: str, status: ConfirmStatusCode) -> Optional[ConfirmCode]:
        query = select(ConfirmCode).where(
            (ConfirmCode.id == code_id) & (ConfirmCode.status == status) & (ConfirmCode.code == code)
        )
        result = await self.session.execute(query)
        fetched = result.fetchone()

        if fetched is None:
            return None

        return fetched[0]
