import pytest
from aiohttp import web

from api.main import api_factory


@pytest.mark.asyncio(loop_scope="function")
async def test_init_app(aiohttp_client, test_config):
    app = await api_factory(test_config)

    assert isinstance(app, web.Application), "App is not an instance of web.Application"

    assert "config" in app, "App config is missing"
    assert app["config"].REDIS.REDIS_HOST == "localhost", "Redis host config is incorrect"

    assert len(app.middlewares) > 0, "No middlewares were added to the app"
    assert any(mw.__name__ == "error_middleware" for mw in app.middlewares), "error_middleware is missing"
    assert any(mw.__name__ == "db_session_middleware" for mw in app.middlewares), "db_session_middleware is missing"

    client = await aiohttp_client(app)
    resp = await client.get("/health")
    assert resp.status == 200, f"Expected status 200, got {resp.status}"
    json_resp = await resp.json()
    assert json_resp["status"] == True, "Health check response is incorrect"
