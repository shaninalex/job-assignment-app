from typing import Self, Tuple, Union

from pydantic import BaseModel, EmailStr, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Company
from app.db.models.user import ConfirmCode, User
from app.enums import CompanyStatus, Role, AuthStatus, ConfirmStatusCode
from app.utilites.generate_random_code import generate_numeric_code
from app.utilites.password import is_password_valid, create_password_hash


class CreateCompanyPayload(BaseModel):
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


async def get_company_by_id(session: AsyncSession, company_id: int) -> Union[Company, None]:
    q = await session.execute(select(Company).where(Company.id == company_id))
    return q.scalar_one_or_none()


async def get_company_by_email(session: AsyncSession, company_email: str) -> Union[Company, None]:
    q = await session.execute(select(Company).where(Company.email == company_email))
    return q.scalar_one_or_none()


async def create_company(session: AsyncSession, payload: CreateCompanyPayload) -> Tuple[Company, User, ConfirmCode]:
    if await get_company_by_email(session, payload.email):
        raise ValueError("company already exist")

    company = Company(
        name=payload.name,
        email=payload.email,
        website=payload.website,
        status=CompanyStatus.PENDING,
    )
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=create_password_hash(payload.password),
        role=Role.COMPANY_ADMIN,
        status=AuthStatus.PENDING,
    )
    confirm_code = ConfirmCode(
        user=user,
        code=generate_numeric_code(6),
        status=ConfirmStatusCode.CREATED,
    )
    session.add_all([company, user, confirm_code])
    await session.commit()
    await session.refresh(company)
    await session.refresh(user)
    await session.refresh(confirm_code)
    return company, user, confirm_code


# TODO: update, deactivate ( delete is not a right way )
