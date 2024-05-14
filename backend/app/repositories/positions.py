from typing import List

from app.db import skills, position_skills
from app.models import Position, PositionSkill
from app.repositories import skills as skills_repository


async def position_skills_all(conn) -> List[PositionSkill]:
    query = position_skills.select()
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[PositionSkill] = []
    for d in data:
        out.append(PositionSkill(**d))
    return out


async def position_skills_by_post_id(conn, id: int) -> List[PositionSkill]:
    query = position_skills.select().where(position_skills.c.position_id == id)
    results = await conn.execute(query)
    data = await results.fetchall()
    out: List[PositionSkill] = []
    for d in data:
        out.append(PositionSkill(**d))
    return out


async def all(conn) -> List[Position]:
    # get all positions, skills and thair relation table - position_skills
    # then for/in them and attach skills for positions by position_skills ids
    query = skills.select()
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
