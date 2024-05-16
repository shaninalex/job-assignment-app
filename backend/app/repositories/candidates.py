from typing import List

from app.models import ApplyPayload, Skill, Candidate
from app.db import candidates, candidates_skills
from app.repositories import skills as skills_repository, pos


async def save_candidate_skills(conn, candidate_id: int, skills: List[Skill]):
    for s in skills:
        query = candidates_skills.insert().values(
            candidate_id=candidate_id,
            skill=s.id,
        )
        await conn.execute(query)


async def save(conn, payload: ApplyPayload):
    query = candidates.insert().values(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        about=payload.about,
        position_id=payload.position_id,
    )
    res = await conn.execute(query)
    result = await res.fetchone()
    candidate_id = result[0]

    if payload.skills:
        candidate_skills = await skills_repository.save_skills_list(conn, payload.skills)
        await save_candidate_skills(conn, candidate_id, candidate_skills)


async def all(conn) -> List[Candidate]:
    query = candidates.select()
    res = await conn.execute(query)
    results = await res.fetchall()

    cc: List[Candidate] = []
    for c in results:
        # TODO: extract position object
        position = await pos.get(conn, c[6])
        print(position)
        cc.append(Candidate(
            id=c[0],
            name=c[1],
            email=c[2],
            phone=c[3],
            about=c[4],
            submitted=c[5],
            position=position.to_json(),
            created_at=str(c[7]),
        ))

    return cc
