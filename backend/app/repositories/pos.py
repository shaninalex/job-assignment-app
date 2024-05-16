from typing import List

from app.db import position_skills, position, skills
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


async def create_position_skill(conn, position: Position, skill: Skill):
    q = position_skills.insert().values(
        position_id=position.id,
        skill=skill.id,
    )
    await conn.execute(q)


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
        for s in [si for si in position_skills_list if si.position_id == p.id]:
            for a in all_skills:
                if s.skill == a.id:
                    p.skills.append(a)
                    break

    return out


async def create(conn, payload: Position) -> Position:
    query = position.insert().values(
        name=payload.name,
        description=payload.description,
    )

    result = await conn.execute(query)
    data = await result.fetchone()
    payload.id = data[0]

    if payload.skills:
        for s in payload.skills:
            skill = await skills_repository.get_skill(conn, name=s.name)
            if not skill:
                skill = await skills_repository.create(conn, s)
            await create_position_skill(conn, payload, skill)
            s.id = skill.id

    return payload


async def get(conn, id: int) -> Position:
    query = position.select().where(position.c.id == id)
    result = await conn.execute(query)
    data = await result.fetchone()
    pos = Position(**data)

    rows = await conn.execute(
        position_skills.select().where(position_skills.c.position_id == pos.id)
    )
    data = await rows.fetchall()
    skills_ids = [d[1] for d in data]

    skills_from_db = await conn.execute(
        skills.select().where(skills.c.id.in_(skills_ids))
    )
    skills_results = await skills_from_db.fetchall()
    skills_list: List[Skill] = []
    for s in skills_results:
        skills_list.append(Skill(id=s[0], name=s[1]))

    pos.skills = skills_list

    return pos
