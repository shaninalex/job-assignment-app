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

    def __init__(self):
        super().__init__(ConfirmCode)

    async def get_code(
        self, session: AsyncSession, code_id: str, code: str, status: ConfirmStatusCode
    ) -> Optional[ConfirmCode]:
        query = select(ConfirmCode).where(
            (ConfirmCode.id == code_id) & (ConfirmCode.status == status) & (ConfirmCode.code == code)
        )
        result = await session.execute(query)
        fetched = result.fetchone()

        if fetched is None:
            return None

        return fetched[0]
