from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pkg.consts import ConfirmStatusCode
from pkg.database import ConfirmCode


async def get_confirm_code(
    session: AsyncSession, id: str, code: str, status: ConfirmStatusCode
) -> Optional[ConfirmCode]:
    query = select(ConfirmCode).where(
        (ConfirmCode.id == id)
        & (ConfirmCode.status == status)
        & (ConfirmCode.code == code)
    )
    result = await session.execute(query)
    fetched = result.fetchone()

    if fetched is None:
        return None

    return fetched[0]
