from typing import Self, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Company, CompanyMember
from app.db.models.user import ConfirmCode, User
from app.db.operations.user_op import get_user_by_id
from app.db.session import ServiceError
from app.enums import CompanyStatus, Role, AuthStatus, ConfirmStatusCode, CompanyMemberStatus
from app.utilites.generate_random_code import generate_numeric_code, generate_string_code
from app.utilites.password import is_password_valid, create_password_hash


class CompanyNotFoundError(ServiceError):
    pass


class CompanyMemberAlreadyExists(ServiceError):
    pass


async def get_company_by_id(session: AsyncSession, company_id: UUID) -> Company:
    q = await session.execute(select(Company).where(Company.id == company_id).options(selectinload(Company.members)))
    company = q.scalar_one_or_none()
    if company is None:
        raise CompanyNotFoundError(f"Company with ID {company_id} not found.")
    return company


async def get_company_by_email(session: AsyncSession, company_email: str) -> Company:
    q = await session.execute(select(Company).where(Company.email == company_email))
    company = q.scalar_one_or_none()
    if company is None:
        raise CompanyNotFoundError(f"Company with email {company_email} not found.")
    return company


class CreateCompanyPayload(BaseModel, extra="forbid"):
    name: str
    website: str  # pydantic.HttpUrl ?
    email: EmailStr
    company_admin_name: str
    company_admin_email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not is_password_valid(self.password, self.password_confirm):
            raise ValueError("passwords do not match")
        return self


async def create_company(session: AsyncSession, payload: CreateCompanyPayload) -> Tuple[Company, User, ConfirmCode]:
    try:
        await get_company_by_email(session, payload.email)
    except CompanyNotFoundError:
        pass

    company = Company(
        name=payload.name,
        email=payload.email,
        website=payload.website,
        status=CompanyStatus.PENDING,
    )
    user = User(
        name=payload.company_admin_name,
        email=payload.company_admin_email,
        password_hash=create_password_hash(payload.password),
        role=Role.COMPANY_ADMIN,
        status=AuthStatus.PENDING,
    )
    confirm_code = ConfirmCode(
        user=user,
        code=generate_numeric_code(6),
        key=generate_string_code(128),
        status=ConfirmStatusCode.CREATED,
    )

    company_member = CompanyMember(company=company, user=user, status=CompanyMemberStatus.ACTIVE)
    session.add_all([company, user, confirm_code, company_member])
    await session.flush()
    return company, user, confirm_code


class CreateCompanyMemberPayload(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    role: Role
    password: str
    password_confirm: str
    company_id: UUID

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not is_password_valid(self.password, self.password_confirm):
            raise ValueError("passwords do not match")
        return self


async def create_member(
    session: AsyncSession, payload: CreateCompanyMemberPayload
) -> Tuple[User, ConfirmCode]:
    company = await get_company_by_id(session, payload.company_id)

    # check is user already exist in company members
    for member in company.members:
        if member.user.email == payload.email:
            raise CompanyMemberAlreadyExists(f"Company member {payload.email} already exist")

    # create user
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=create_password_hash(payload.password),
        role=payload.role,
        status=AuthStatus.PENDING,
    )
    confirm_code = ConfirmCode(user=user, code=generate_numeric_code(6), key=generate_string_code(128), status=ConfirmStatusCode.CREATED)
    company_member = CompanyMember(company=company, user=user, status=CompanyMemberStatus.ACTIVE)

    session.add_all([company, user, confirm_code, company_member])
    await session.flush()
    return user, confirm_code


async def add_member(
    session: AsyncSession, company_id: UUID, user_id: UUID, role: Role
) -> Tuple[User, CompanyMember]:
    company = await get_company_by_id(session, company_id)

    for member in company.members:
        if member.user_id == user_id:
            raise CompanyMemberAlreadyExists(f"Company member with ID {user_id} already exist")

    user = await get_user_by_id(session, user_id)
    user.role = role
    company_member = CompanyMember(company_id=company_id, user_id=user_id, status=CompanyMemberStatus.ACTIVE)
    session.add(company_member)
    session.add(user)
    await session.flush()
    return user, company_member


async def delete_member(session: AsyncSession, company_id: UUID, user_id: UUID):
    stmt = delete(CompanyMember).where((CompanyMember.company_id == company_id) & (CompanyMember.user_id == user_id))
    await session.execute(stmt)


# TODO: update, deactivate ( delete is not a right way )
