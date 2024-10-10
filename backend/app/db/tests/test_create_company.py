import uuid

import pytest

from app.db.operations.company import CreateCompanyPayload, create_company
from app.db.operations.user import get_user_by_email
from app.enums import AuthStatus, CompanyStatus, ConfirmStatusCode, Role
from app.utilites.password import check_password


@pytest.mark.asyncio
async def test_create_company(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            website=f"https://{str(u)}.com",
            company_admin_name=str(u),
            company_admin_email=f"{str(u)}@test.com",
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
        assert user.email == payload.email
        assert user.name == payload.name
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
