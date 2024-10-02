from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.routes.public._types import RegistrationPayload
from pkg import password, utils
from pkg.consts import AuthStatus, ConfirmStatusCode, Role
from pkg.database import User
from pkg.database.models import Candidate, ConfirmCode


async def get_user(session: AsyncSession, **kwargs) -> Optional[User]:
    stmt = select(User).options(
        selectinload(User.manager),
    )

    if len(kwargs) == 0:
        return None

    if "id" in kwargs:
        stmt = stmt.where(User.id == kwargs["id"])

    if "email" in kwargs:
        stmt = stmt.where(User.email == kwargs["email"])

    if "active" in kwargs:
        stmt = stmt.where(User.active == kwargs["active"])

    if "status" in kwargs:
        stmt = stmt.where(User.status == kwargs["status"])

    result = await session.scalars(stmt)
    user = result.one_or_none()
    return user


async def create_candidate(
    session: AsyncSession, payload: RegistrationPayload
) -> Tuple[User, Candidate]:
    user = User(
        name=payload.name,
        email=payload.email,
        role=Role.CANDIDATE,
        status=AuthStatus.PENDING,
        password_hash=password.get_hashed_password(payload.password),
        codes=[
            ConfirmCode(
                code=utils.generate_code(6),
                status=ConfirmStatusCode.CREATED,
            )
        ],
    )
    session.add(user)
    candidate = Candidate(user=user)
    candidate.experiences = []
    session.add(candidate)
    await session.commit()
    return user, candidate


async def confirm_user(session: AsyncSession, code: ConfirmCode) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == code.user_id))
    users = result.fetchone()

    if users is None:
        return None

    user = users[0]

    user.confirmed = True
    user.status = AuthStatus.ACTIVE
    code.status = ConfirmStatusCode.USED

    await session.commit()

    # Ensure objects are still attached to the session if needed
    await session.refresh(user)
    await session.refresh(code)

    return user
