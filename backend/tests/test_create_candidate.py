import pytest

from api.main import api_factory
from pkg.consts import Role, AuthStatus


@pytest.mark.asyncio(loop_scope="function")
async def test_init_app(aiohttp_client, test_config, cleanup):
    app = await api_factory(test_config)
    payload = {
        "name": "test_name",
        "email": "test@test.com",
        "password": "testPassword",
        "password_confirm": "testPassword",
        "type": "candidate",
    }
    client = await aiohttp_client(app)
    resp = await client.post("/api/auth/register", json=payload)
    assert resp.status == 200, f"Expected status 200, got {resp.status}"

    data = await resp.json()

    assert data["data"]["user"]["role"] == Role.CANDIDATE.name
    assert data["data"]["user"]["email"] == payload["email"]
    assert data["data"]["user"]["name"] == payload["name"]
    assert data["data"]["user"]["active"] == True
    assert data["data"]["user"]["status"] == AuthStatus.PENDING.name.lower()
