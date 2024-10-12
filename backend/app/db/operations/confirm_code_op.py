from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.user import ConfirmCode
from app.exceptions.exceptions import ConfirmCodeNotFound


async def get_confirm_code(session: AsyncSession, key: str, code: str):
    q = await session.execute(
        select(ConfirmCode)
        .where((ConfirmCode.code == code) & (ConfirmCode.key == key))
        .options(selectinload(ConfirmCode.user))
    )
    confirm_code = q.scalar_one_or_none()
    if not confirm_code:
        raise ConfirmCodeNotFound()

    return confirm_code
