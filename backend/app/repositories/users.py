from datetime import datetime
from sqlalchemy import insert, select
from app.db import users
from app.pkg import password
from app.models import AdminCreateUserPayload, User


async def create(connection, payload: AdminCreateUserPayload) -> bool:
    hashed_password = password.get_hashed_password(payload.password)
    query = insert(users).values(
        email=payload.email,
        password=hashed_password,
    )

    try:
        await connection.execute(query)
        return True
    except Exception as e:
        print(e)
        return False
