import jwt
import pytest
from sqlalchemy import select

from api.main import api_factory
from pkg.consts import ConfirmStatusCode, Role, AuthStatus
from pkg.models.models import ConfirmCode


@pytest.mark.asyncio(loop_scope="function")
async def test_register_company(aiohttp_client, test_config, async_session, test_app, cleanup):
    payload = {
        "name": "testCompany",
        "email": "testCompany@gmail.com",
        "password": "123",
        "password_confirm": "123",
        "type": "company_admin",
        "company_name": "ABC",
    }
    client = await aiohttp_client(test_app)
    resp = await client.post("/api/auth/register", json=payload)
    assert resp.status == 200, f"Expected status 200, got {resp.status}"

    data = await resp.json()
    user_data = data["data"]["user"]
    assert user_data["id"] != ""
    assert data["data"]["user"]["role"] == Role.COMPANY_ADMIN.name
    assert data["data"]["user"]["email"] == payload["email"]
    assert data["data"]["user"]["name"] == payload["name"]
    assert data["data"]["user"]["active"] == True
    assert data["data"]["user"]["status"] == AuthStatus.PENDING.name.lower()

    async with async_session as session:
        confirm_code_query = select(ConfirmCode).where(
            (ConfirmCode.user_id == user_data["id"]) &
            (ConfirmCode.status == ConfirmStatusCode.SENT)
        )
        result = await session.execute(confirm_code_query)
        confirm_code = result.scalars().first()
        assert confirm_code is not None, "Confirm code not found in the database"
        assert confirm_code.id != None
        assert confirm_code.user_id != None
        assert confirm_code.code != None
        assert len(confirm_code.code) == 6

        resp = await client.post("/api/auth/confirm", json={
            "id": str(confirm_code.id),
            "code": confirm_code.code,
        })
        assert resp.status == 200, f"Expected status 200, got {resp.status}"
    
    resp = await client.post("/api/auth/login", json={
        "email": payload["email"],
        "password": payload["password"],
    })

    assert resp.status == 200, f"Expected status 200, got {resp.status}"
    data = await resp.json()

    assert "token" in data["data"]
    assert "user" in data["data"]
    assert "company" in data["data"]

    assert data["data"]["user"]["status"] == AuthStatus.ACTIVE.name.lower()
    assert data["data"]["user"]["role"] == Role.COMPANY_ADMIN.name
    assert data["data"]["user"]["email"] == payload["email"]
    assert data["data"]["user"]["name"] == payload["name"]

    claims = jwt.decode(data["data"]["token"], test_config.APP_SECRET, algorithms=["HS256"])
    assert claims["sub"] == user_data["id"]
    assert claims["roles"] == [Role.COMPANY_ADMIN.name.lower()]
