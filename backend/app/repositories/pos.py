from typing import List

from app.db import skills, position_skills, position
from app.models import Position, PositionSkill, Skill
from app.repositories import skills as skills_repository


async def position_skills_all(conn) -> List[PositionSkill]:
    query = position_skills.select()
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[PositionSkill] = []
    for d in data:
        out.append(PositionSkill(**d))
    return out


async def get_skill(conn, id: int = None, name: str = None) -> Skill | None:
    query = skills.select()
    if id:
        query = query.where(skills.c.id == id)
    elif name:
        query = query.where(skills.c.name == name)

    results = await conn.execute(query)
    data = await results.fetchone()
    if not data:
        return None

    out: Skill = Skill(**data)
    return out


async def position_skills_by_post_id(conn, id: int) -> List[PositionSkill]:
    query = position_skills.select().where(position_skills.c.position_id == id)
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[PositionSkill] = []
    for d in data:
        out.append(PositionSkill(**d))
    return out


async def create_position_skill(conn, position: Position, skill: Skill) -> PositionSkill:
    q = position_skills.insert().values(
        position_id=position.id,
        skill=skill.id
    )
    results = await conn.execute(q)
    data = await results.fetchone()
    return PositionSkill(**data)


async def all(conn) -> List[Position]:
    # get all positions, skills and their relation table - position_skills
    # then for/in them and attach skills for positions by position_skills ids
    query = position.select()
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[Position] = []

    for d in data:
        out.append(Position(**d))

    all_skills = await skills_repository.all(conn)
    position_skills_list = await position_skills_all(conn)

    for p in out:
        skills_ids = [
            si for si in position_skills_list if si.position_id == p.id]
        p.skills = [s for s in all_skills if s in skills_ids]
    return out


async def create(conn, payload: Position) -> Position:
    query = position.insert().values(
        name=payload.name,
        description=payload.description,
    )

    result = await conn.execute(query)
    data = await result.fetchone()
    payload.id = data[0]

    for s in payload.skills:
        skill = get_skill(conn, s.name)
        if skill:
            await create_position_skill(conn, position, skill)
        else:
            skill = await skills_repository.create(conn, s)
            await create_position_skill(conn, position, skill)

    return payload


async def get(conn, id: int) -> Position:
    query = position.select().where(position.c.id == id)
    result = await conn.execute(query)
    data = await result.fetchone()
    return Position(**data)
