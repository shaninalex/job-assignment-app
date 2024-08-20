from typing import Tuple
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.types import RegisterForm
from pkg import password
from database import Company, CompanyManager, Auth, AuthStatus, Candidate, CompanyManagerRole


async def create_company(
        session: async_sessionmaker[AsyncSession],
        payload: RegisterForm,
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
        session: async_sessionmaker[AsyncSession],
        payload: RegisterForm,
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
        session.add(candidate)
        await session.commit()
        return auth, candidate
