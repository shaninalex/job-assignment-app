import logging

from datetime import datetime
from typing import List

from app.db import Role, users
from app.pkg import password
from app.models import AdminCreateUserPayload, User


async def create(connection, payload: AdminCreateUserPayload) -> User:
    hashed_password = password.get_hashed_password(payload.password)
    query = users.insert().values(
        email=payload.email,
        password=hashed_password,
    )

    row = await connection.execute(query)
    result = await row.fetchone() # get result id
    new_user = User(
        id=result[0],
        email=payload.email,
        role=Role.manager,
        created_at=datetime.now(),
    )
    return new_user


async def list(connection) -> List[dict]:
    query = users.select()
    row = await connection.execute(query)
    result = await row.fetchall()

    list_users: List[dict] = []
    for u in result:
        user: User = User(**u)
        list_users.append(user.to_json())

    return list_users
