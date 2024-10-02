from typing import Optional, Tuple, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.routes.public._types import RegistrationPayload
from pkg import password, utils
from pkg.consts import AuthStatus, ConfirmStatusCode, Role
from pkg.database.models import Company, CompanyManager, ConfirmCode, User


async def get_company(session: AsyncSession, **kwargs) -> Optional[Company]:
    stmt = select(Company).options(
        selectinload(Company.managers),
    )

    if "id" in kwargs:
        stmt = stmt.where(Company.id == kwargs["id"])

    result = await session.scalars(stmt)
    company = result.one_or_none()
    return company


async def get_companies(session: AsyncSession, **kwargs) -> Sequence[Company]:
    stmt = select(Company)
    # TODO: handle kwargs
    result = await session.scalars(stmt)
    companies = result.all()
    return companies


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
