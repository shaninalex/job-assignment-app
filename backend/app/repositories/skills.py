import logging
from typing import List

from app.db import skills
from app.models import Skill


async def all(conn) -> List[Skill]:
    query = skills.select()
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[Skill] = []

    for d in data:
        out.append(Skill(**d))

    return out


async def create(conn, payload: Skill) -> Skill:
    query = skills.insert().values(name=payload.name)
    results = await conn.execute(query)
    data = await results.fetchone()
    payload.id = data[0]
    return payload


async def delete(conn, id: int) -> None:
    query = skills.delete().where(skills.c.id == id)
    await conn.execute(query)
    return


async def patch(conn, payload: Skill) -> Skill:
    query = skills.update().values(name=payload.name).where(skills.c.id == payload.id)
    await conn.execute(query)
    return payload


async def get_skill(conn, id: int | None = None, name: str | None = None) -> Skill | None:
    query = skills.select()
    if id:
        query = query.where(skills.c.id == id)
    elif name:
        query = query.where(skills.c.name == name)

    results = await conn.execute(query)
    data = await results.fetchone()

    if not data:
        return None

    out: Skill = Skill(id=data[0], name=data[1])
    return out
