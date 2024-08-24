from typing import Tuple, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.types import RegistrationPayload
from database import (
    Company,
    CompanyManager,
    User,
    Candidate,
    ConfirmCode,
)
from globalTypes.consts import Role, ConfirmStatusCode, AuthStatus
from pkg import password, utils


async def create_company(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Company, User, CompanyManager]:
    user = User(
        name=payload.name,
        email=payload.email,
        role=Role.COMPANY_MANAGER,
        status=AuthStatus.PENDING,
        password_hash=password.get_hashed_password(payload.password),
        codes=[
            ConfirmCode(
                email=payload.email,
                code=utils.generate_code(6),
                status=ConfirmStatusCode.CREATED,
            )
        ],
    )
    session.add(user)

    # TODO: for some reason this function return company without name. But it has name in db...
    company = Company(name=payload.companyName)
    session.add(company)

    member = CompanyManager(
        company=company,
        user=user,
    )
    session.add(member)

    await session.commit()
    return company, user, member


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
                email=payload.email,
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