from app import models
from app.pkg import password, jwt
from app.db import users, RecordNotFound
from sqlalchemy import select


async def login(connection,
                payload: models.LoginPayload) -> models.JWTTokenResponse | None:
    """
    Logs in the user.
    Parameters
    ----------
    payload : LoginPayload
        Validated user login payload
    Returns
    -------
    list
        signed JWT access/refresh tokens packed in JWTTokenResponse type
    """
    query = select(users).where(users.c.email == payload.email)
    result = await connection.execute(query)
    data = await result.fetchone()
    if not data:
        raise RecordNotFound

    if not password.check_password(payload.password, data['password']):
        return None

    user = models.User(**data)
    token = jwt.create_jwt_token(user)
    return token
