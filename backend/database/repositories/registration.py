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
    CompanyManagerRole, ConfirmCode,
)


async def create_company(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Company, User, CompanyManager]:
    async with session:
        company = Company(name=payload["companyName"])
        session.add(company)
        user = User(
            name=payload["name"],
            password_hash=password.get_hashed_password(payload["password"]),
            email=payload["email"],
            role=Role.COMPANY_ADMIN
        )
        session.add(user)
        await session.commit()
        member = CompanyManager(
            name=payload["name"],
            email=payload["email"],
            user_id=user.id,
            company_id=company.id,
            role=CompanyManagerRole.ADMIN,
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
            name=payload["name"],
            email=payload["email"],
            role=Role.CANDIDATE,
            password_hash=password.get_hashed_password(payload["password"]),
            codes=[ConfirmCode(
                email=payload["email"],
                code=utils.generate_code(6),
                status=ConfirmStatusCode.SENDED,
            )]
        )
        session.add(user)
        candidate = Candidate(user_id=user.id)
        candidate.experiences = []
        session.add(candidate)
        await session.commit()
        return user, candidate

