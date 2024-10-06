import uuid
import pytest
from sqlalchemy import select
from api.main import api_factory
from pkg.consts import ConfirmStatusCode, Role
from pkg.jwt import create_jwt_token
from pkg.models.models import ConfirmCode, User


@pytest.mark.asyncio(loop_scope="function")
async def test_unauthorized_post_request_on_guarded_endpoint(aiohttp_client, test_config, async_session):
    app = await api_factory(test_config)
    payload = {"invalid": "payload"}
    client = await aiohttp_client(app)

    # test_unauthorized_post_request_on_guarded_endpoint
    resp = await client.post("/api/company/position", json=payload)
    data = await resp.json()
    assert data["data"] == None
    assert resp.status == 401, f"Expected status not 200, got {resp.status}"
    assert data["messages"] == ["Unauthorized"]

    # test_invalid_jwt
    resp = await client.post("/api/company/position", json=payload, headers={"Authorization": "123"})
    data = await resp.json()
    assert data["data"] == None
    assert resp.status == 401, f"Expected status not 200, got {resp.status}"
    assert data["messages"] == ["Invalid token"]

    # test_invalid_jwt_token
    resp = await client.post("/api/company/position", json=payload, headers={"Authorization": "Bearer 123"})
    data = await resp.json()
    assert data["data"] == None
    assert resp.status == 401, f"Expected status not 200, got {resp.status}"
    assert data["messages"] == ["Invalid token"]

    # test_invalid_jwt_token_claims
    # JWT TOKEN CLAIMS
    # {
    #   "sub": "1234567890",
    #   "name": "John Doe",
    #   "iat": 1516239022
    # }
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    resp = await client.post("/api/company/position", json=payload, headers={"Authorization": token})
    data = await resp.json()
    assert data["data"] == None
    assert resp.status == 401, f"Expected status not 200, got {resp.status}"
    assert data["messages"] == ["Invalid token"]

    # test_invalid_jwt_user
    user = User(id=uuid.uuid4(), role=Role.COMPANY_ADMIN)
    token = create_jwt_token(test_config.APP_SECRET, user)
    resp = await client.post("/api/company/position", json=payload, headers={"Authorization": token})
    data = await resp.json()
    assert data["data"] == None
    assert resp.status == 401, f"Expected status not 200, got {resp.status}"
    assert data["messages"] == ["User not found"]

    # test_registered_user_candidate_access_role_specific_endpoint
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
    user_data = data["data"]["user"]

    confirm_code_query = select(ConfirmCode).where(
        (ConfirmCode.user_id == user_data["id"]) & (ConfirmCode.status == ConfirmStatusCode.SENT)
    )
    result = await async_session.execute(confirm_code_query)
    confirm_code = result.scalars().first()
    resp = await client.post(
        "/api/auth/confirm",
        json={
            "id": str(confirm_code.id),
            "code": confirm_code.code,
        },
    )

    resp = await client.post(
        "/api/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )
    login_data = await resp.json()

    payload = {"dummy": "data"}
    resp = await client.post(
        "/api/company/position", json=payload, headers={"Authorization": login_data["data"]["token"]}
    )

    assert resp.status == 403, f"Expected status not 200, got {resp.status}"
    data = await resp.json()
    assert data["data"] == None
    assert data["messages"] == ["Invalid token"]
