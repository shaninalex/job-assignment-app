from typing import List

from app.models import Skill as SkillModel
from app.db import Skill


def get_or_create_skills(session, payload: List[SkillModel]) -> List[Skill]:
    skills: List[Skill] = []
    for skill in payload:
        db_skill = session.query(Skill).filter(Skill.name == skill.name).first()
        if db_skill:
            skills.append(db_skill)
        else:
            s = Skill(name=skill.name)
            session.add(s)
            session.commit()
            skills.append(s)

    return skills

