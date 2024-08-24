from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from api.types import RegistrationPayload
from globalTypes.consts import Role, ConfirmStatusCode
from pkg import password, utils
from database import (
    Company,
    CompanyManager,
    User,
    Candidate,
    ConfirmCode,
)


async def create_company(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Company, User, CompanyManager]:
    async with session:
        user = User(
            name=payload.name,
            email=payload.email,
            role=Role.COMPANY_MANAGER,
            password_hash=password.get_hashed_password(payload.password),
            codes=[ConfirmCode(
                email=payload.email,
                code=utils.generate_code(6),
                status=ConfirmStatusCode.SENDED,
            )]
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
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[User, Candidate]:
    async with session:
        user = User(
            name=payload.name,
            email=payload.email,
            role=Role.CANDIDATE,
            password_hash=password.get_hashed_password(payload.password),
            codes=[ConfirmCode(
                email=payload.email,
                code=utils.generate_code(6),
                status=ConfirmStatusCode.SENDED,
            )]
        )
        session.add(user)
        candidate = Candidate(
            user=user
        )
        candidate.experiences = []
        session.add(candidate)
        await session.commit()
        return user, candidate
