from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.public.types import RegistrationPayload
from database.models import Company, CompanyManager, ConfirmCode, User
from globalTypes.consts import AuthStatus, ConfirmStatusCode, Role
from pkg import password, utils


async def get_company(session: AsyncSession, **kwargs) -> Optional[Company]: 
    stmt = select(Company).options(
        selectinload(Company.managers),
    )

    if len(kwargs) == 0:
        return None

    if "id" in kwargs:
        stmt = stmt.where(Company.id == kwargs["id"])

    result = await session.scalars(stmt)
    company = result.one_or_none()
    return company


async def create_company(
    session: AsyncSession,
    payload: RegistrationPayload,
) -> Tuple[Company, User, CompanyManager]:
    user = User(
        name=payload.name,
        email=payload.email,
        role=Role.COMPANY_ADMIN,
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
    company = Company(name=payload.company_name)
    session.add(company)

    member = CompanyManager(
        company=company,
        user=user,
    )
    session.add(member)

    await session.commit()
    return company, user, member

