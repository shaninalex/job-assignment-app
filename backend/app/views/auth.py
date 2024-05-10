from http import HTTPStatus
from aiohttp import web
from pydantic import ValidationError
from app.repositories.auth import AuthRepository

from app.models import LoginPayload

def setup_auth_routes(app: web.Application):
    app.router.add_post('/api/auth/login', login_user)
    app.router.add_post('/api/auth/refresh', refresh_token)


async def login_user(request: web.Request):
    data = await request.json()  # form data
    try:
        payload: LoginPayload = LoginPayload(**data)
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            error_messages.append({
                "field": error["loc"][0],
                "error_message": error["msg"]
            })
        return web.json_response({"errors": error_messages}, status=HTTPStatus.BAD_REQUEST)
    
    response = AuthRepository(connection=None).login(payload)
    return web.json_response(response.model_dump(), status=HTTPStatus.OK)

async def refresh_token(request):
    return web.json_response({"token": "refreshed jwt"})