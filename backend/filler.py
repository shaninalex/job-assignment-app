"""
Script to fill database with data
"""

import asyncio
import random

from faker import Faker
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Company, Base
from app.db.operations.company_op import CreateCompanyPayload, create_company
from app.db.operations.position_op import PositionCreatePayload, position_create
from app.db.operations.user_op import create_user, UserPayload
from app.db.session import DatabaseSessionManager
from app.enums import (
    AuthStatus,
    ConfirmStatusCode,
    CompanyStatus,
    Remote,
    PositionStatus,
    TravelRequired,
    WorkingHours,
    SalaryType,
    Role,
)

COMPANIES_NUMBER = 136
POSITION_FOR_EACH_COMPANY = 12
CANDIDATES_NUMBER = 200

fake = Faker("en_US")

db = DatabaseSessionManager(settings.database_url)


async def clear_db(db: DatabaseSessionManager):
    async with db.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


async def create_position_item(session: AsyncSession, company: Company):
    payload = PositionCreatePayload(
        title=fake.job(),
        company_id=company.id,
        description=fake.text(),
        interview_stages=fake.text(),
        responsibilities=fake.text(),
        requirements=fake.text(),
        price_range=fake.text(max_nb_chars=90),
        offer=fake.text(),
        remote=random.choice(list(Remote)),
        salary=random.choice(list(SalaryType)),
        hours=random.choice(list(WorkingHours)),
        travel=random.choice(list(TravelRequired)),
        status=PositionStatus.ACTIVE,
    )
    logger.info(payload.title)
    await position_create(session, payload)


# Create 12 companies
async def create_companies(session: AsyncSession):
    for c in range(COMPANIES_NUMBER):
        company_name = fake.company()
        domain = company_name.lower().replace(",", "").replace(" ", "-").replace("'", "") + ".com"
        website = f"https://{domain}"
        email = f"hello@{domain}"
        admin_first_name = fake.first_name_male()
        admin_last_name = fake.last_name_male()
        admin_name = f"{admin_first_name} {admin_last_name}"
        admin_email = f"{admin_first_name.lower()}@{domain}"
        admin_password = "password"
        payload = CreateCompanyPayload(
            name=company_name,
            website=website,
            email=email,
            company_admin_name=admin_name,
            company_admin_email=admin_email,
            password=admin_password,
            password_confirm=admin_password,
        )
        logger.info(f"{c}: Company - {email}")
        company, user, confirm_code = await create_company(session, payload)
        company.status = CompanyStatus.ACTIVE
        user.status = AuthStatus.ACTIVE
        confirm_code.status = ConfirmStatusCode.USED
        for _ in range(POSITION_FOR_EACH_COMPANY):
            await create_position_item(session, company)


# Create 30 candidates
async def create_candidates(session: AsyncSession):
    for u in range(CANDIDATES_NUMBER):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
        password = "password"
        payload = UserPayload(
            name=first_name + last_name,
            email=email,
            password=password,
            password_confirm=password,
        )
        logger.info(f"{u+1}: user - {email}")
        user, confirm_code = await create_user(session, payload, Role.CANDIDATE)
        user.status = AuthStatus.ACTIVE
        user.confirmed = True
        confirm_code.status = ConfirmStatusCode.USED


async def main():
    await clear_db(db)
    async with db.session() as session:
        await create_companies(session)
        await create_candidates(session)


if __name__ == "__main__":
    asyncio.run(main())
