import uuid

import pytest
from sqlalchemy import func, select

from app.db.models import CompanyMember
from app.db.operations.company_op import (
    CreateCompanyMemberPayload,
    CreateCompanyPayload,
    add_member,
    create_company,
    create_member,
    delete_member,
    get_company_members,
    create_company_only,
    patch_company,
    PartialCompanyPayload,
    CreateCompanyOnlyPayload,
    disable_company,
)
from app.db.operations.user_op import UserPayload, create_user, get_user_by_email
from app.enums import Role, AuthStatus, ConfirmStatusCode, CompanyStatus
from app.utilites.password import check_password


@pytest.mark.asyncio
async def test_create_company(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyPayload(
            name=f"company_name_{str(u)}",
            email=f"{str(u)}@company.com",
            website=f"https://{str(u)}.com",
            company_admin_name=f"user_name_{str(u)}",
            company_admin_email=f"user_name_{str(u)}@company.com",
            password="testtest",
            password_confirm="testtest",
        )
        company, user, confirm_code = await create_company(session, payload)

        # test company
        assert company is not None
        assert company.name == payload.name
        assert company.email == payload.email
        assert company.website == payload.website
        assert company.status == CompanyStatus.PENDING
        assert company.image_link is None

        # test company admin
        assert user is not None
        assert user.id is not None
        assert user.email == payload.company_admin_email
        assert user.name == payload.company_admin_name
        assert user.password_hash != payload.password
        assert check_password(payload.password, user.password_hash)
        assert user.role == Role.COMPANY_ADMIN
        assert user.status == AuthStatus.PENDING
        new_user = await get_user_by_email(session, user.email)
        assert new_user is not None

        # test new user code
        assert confirm_code is not None
        assert confirm_code.status == ConfirmStatusCode.CREATED
        assert new_user.codes is not None
        assert len(new_user.codes) == 1
        assert new_user.codes[0].status == ConfirmStatusCode.CREATED
        assert new_user.codes[0].code == confirm_code.code


@pytest.mark.asyncio
async def test_create_member(session):
    async with session() as session:
        u = uuid.uuid4()
        company_payload = CreateCompanyPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            website=f"https://{str(u)}.com",
            company_admin_name=str(u),
            company_admin_email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        company, user, confirm_code = await create_company(session, company_payload)

        member_uuid = uuid.uuid4()
        member_payload = CreateCompanyMemberPayload(
            name=str(member_uuid),
            email=f"{str(member_uuid)}@email.com",
            role=Role.COMPANY_MEMBER,
            password="testtest",
            password_confirm="testtest",
            company_id=company.id,
        )

        member, member_confirm_code = await create_member(session, member_payload)
        assert member is not None
        assert member_confirm_code is not None
        assert member.name == member_payload.name
        assert member.role == member_payload.role
        assert member_confirm_code.user_id == member.id


@pytest.mark.asyncio
async def test_add_member(session):
    async with session() as session:
        u = uuid.uuid4()
        company_payload = CreateCompanyPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            website=f"https://{str(u)}.com",
            company_admin_name=str(u),
            company_admin_email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        company, _, _ = await create_company(session, company_payload)
        um = uuid.uuid4()
        payload = UserPayload(
            name=str(um),
            email=f"{str(um)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )

        user, cc = await create_user(session, payload, Role.COMPANY_MEMBER)
        assert user.email == payload.email
        assert user.name == payload.name
        assert user.role == Role.COMPANY_MEMBER

        updated_user, company_member = await add_member(session, company.id, user.id, Role.COMPANY_HR)
        assert updated_user is not None
        assert updated_user.role == Role.COMPANY_HR
        assert updated_user.email == payload.email
        assert company_member.user_id == updated_user.id
        assert company_member.company_id == company.id

        statement = select(func.count()).select_from(CompanyMember)
        result = await session.execute(statement)
        company_members_count = result.scalar()
        assert company_members_count == 2


@pytest.mark.asyncio
async def test_remove_member(session):
    async with session() as session:
        # create company
        u = uuid.uuid4()
        company_payload = CreateCompanyPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            website=f"https://{str(u)}.com",
            company_admin_name=str(u),
            company_admin_email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        company, _, _ = await create_company(session, company_payload)

        # create user without company
        um = uuid.uuid4()
        payload = UserPayload(
            name=str(um),
            email=f"{str(um)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        user, cc = await create_user(session, payload, Role.COMPANY_MEMBER)

        # add member to company
        await add_member(session, company.id, user.id, Role.COMPANY_HR)

        statement = select(func.count()).select_from(CompanyMember)
        result = await session.execute(statement)
        company_members_count = result.scalar()
        assert company_members_count == 2

        # test remove member
        await delete_member(session, company.id, user.id)

        statement = select(func.count()).select_from(CompanyMember)
        result = await session.execute(statement)
        company_members_count = result.scalar()
        assert company_members_count == 1


@pytest.mark.asyncio
async def test_get_company_members(session):
    async with session() as session:
        # create company
        u = uuid.uuid4()
        company_payload = CreateCompanyPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            website=f"https://{str(u)}.com",
            company_admin_name=str(u),
            company_admin_email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        company, _user, _ = await create_company(session, company_payload)
        assert company.id == _user.member.company_id
        members = await get_company_members(session, company.id)
        assert len(members) == 1, f"Expected 1 company member. Got: {len(members)}"


@pytest.mark.asyncio
async def test_create_company_only(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        assert company is not None
        assert company.name == payload.name
        assert company.email == payload.email
        assert company.website == payload.website
        assert company.status == CompanyStatus.PENDING


@pytest.mark.asyncio
async def test_patch_company(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        updates = PartialCompanyPayload(
            name="updated_name",
            website="updated_website",
            email="updated@email.com",
            image_link="updated_image_link",
        )
        updated_company = await patch_company(session, company_id=company.id, payload=updates)
        assert updated_company.name == updates.name
        assert updated_company.email == updates.email
        assert updated_company.website == updates.website
        assert updated_company.image_link == updates.image_link


@pytest.mark.asyncio
async def test_disable_company(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        disabled_company = await disable_company(session, company_id=company.id)
        assert company.status == disabled_company.status
