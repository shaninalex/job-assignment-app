from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from api.types import RegistrationPayload
from pkg import password
from database import (
    Company,
    CompanyManager,
    Auth,
    AuthStatus,
    Candidate,
    CompanyManagerRole,
)


async def create_company(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Company, Auth, CompanyManager]:
    async with session:
        company = Company(name=payload["companyName"])
        session.add(company)
        auth = Auth(
            hash=password.get_hashed_password(payload["password"]),
            email=payload["email"],
            status=AuthStatus.PENDING,
        )
        session.add(auth)
        await session.commit()
        member = CompanyManager(
            name=payload["name"],
            email=payload["email"],
            auth_id=auth.id,
            company_id=company.id,
            role=CompanyManagerRole.ADMIN,
        )
        session.add(member)
        await session.commit()
        return company, auth, member


async def create_candidate(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Auth, Candidate]:
    async with session:
        auth = Auth(
            hash=password.get_hashed_password(payload["password"]),
            email=payload["email"],
            status=AuthStatus.PENDING,
        )
        session.add(auth)
        await session.commit()
        candidate = Candidate(
            name=payload["name"],
            email=payload["email"],
            auth_id=auth.id,
        )
        candidate.experiences = []
        session.add(candidate)
        await session.commit()
        return auth, candidate
