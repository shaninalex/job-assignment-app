from typing import Tuple
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.types import RegisterPayload
from api.pkg.password import get_hashed_password
from database import Company, CompanyManager, Auth, AuthStatus


async def create_company(
        session: async_sessionmaker[AsyncSession],
        payload: RegisterPayload,
) -> Tuple[Company, Auth, CompanyManager]:
    async with session:
        company = Company(name=payload["companyName"])
        session.add(company)
        auth = Auth(
            hash=get_hashed_password(payload["password"]),
            email=payload["email"],
            status=AuthStatus.PENDING,
        )
        session.add(auth)
        await session.commit()
        member = CompanyManager(
            name=payload["name"],
            email=payload["email"],
            auth_id=auth.id,
            company_id=company.id
        )
        session.add(member)
        await session.commit()
        return company, auth, member
