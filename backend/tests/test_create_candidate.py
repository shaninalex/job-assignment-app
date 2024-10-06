import time
import uuid
import jwt
import pytest
from sqlalchemy import select
from api.main import api_factory
from pkg.consts import ConfirmStatusCode, Role, AuthStatus
from pkg.models.models import ConfirmCode


@pytest.mark.asyncio(loop_scope="function")
async def test_create_candidate(aiohttp_client, test_config, async_session):
    app = await api_factory(test_config)
    unique_id = uuid.uuid4()
    payload = {
        "name": f"test_name_{str(unique_id)}",
        "email": f"test_{str(unique_id)}@test.com",
        "password": "testPassword",
        "password_confirm": "testPassword",
        "type": "candidate",
    }
    client = await aiohttp_client(app)
    resp = await client.post("/api/auth/register", json=payload)

    data = await resp.json()
    assert resp.status == 200, f"Expected status 200, got {resp.status}"

    data = await resp.json()
    user_data = data["data"]["user"]
    assert user_data["id"] != ""
    assert user_data["role"] == Role.CANDIDATE.name
    assert user_data["email"] == payload["email"]
    assert user_data["name"] == payload["name"]
    assert user_data["active"] == True
    assert user_data["status"] == AuthStatus.PENDING.name.lower()

    confirm_code_query = select(ConfirmCode).where(
        (ConfirmCode.user_id == user_data["id"]) & (ConfirmCode.status == ConfirmStatusCode.SENT)
    )
    result = await async_session.execute(confirm_code_query)
    confirm_code = result.scalars().first()

    assert confirm_code is not None, "Confirm code not found in the database"
    assert confirm_code.id != None
    assert confirm_code.user_id != None
    assert confirm_code.code != None
    assert len(confirm_code.code) == 6

    resp = await client.post(
        "/api/auth/confirm",
        json={
            "id": str(confirm_code.id),
            "code": confirm_code.code,
        },
    )
    assert resp.status == 200, f"Expected status 200, got {resp.status}"

    resp = await client.post(
        "/api/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert resp.status == 200, f"Expected status 200, got {resp.status}"
    data = await resp.json()

    assert "token" in data["data"]
    assert "user" in data["data"]
    assert "company" not in data["data"]

    assert data["data"]["user"]["status"] == AuthStatus.ACTIVE.name.lower()
    assert data["data"]["user"]["role"] == Role.CANDIDATE.name
    assert data["data"]["user"]["email"] == payload["email"]
    assert data["data"]["user"]["name"] == payload["name"]

    claims = jwt.decode(data["data"]["token"], test_config.APP_SECRET, algorithms=["HS256"])
    assert claims["sub"] == user_data["id"]
    assert claims["roles"] == [Role.CANDIDATE.name.lower()]
