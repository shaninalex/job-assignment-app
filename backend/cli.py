# Cli for backend

# Usage:
#   python cli.py --create-admin
#   python cli.py --create-skills
#   python cli.py --help
import sys
import os
import argparse
from typing import List
from getpass import getpass

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError

from app.db import Role, User, Skill
from app.settings import DATABASE_URI
from app.pkg import password


def create_admin():
    engine = create_engine(DATABASE_URI)

    hashed_password = password.get_hashed_password(
        getpass(prompt='Input your password: '))
    user: User = User(
        email=os.getenv("ADMIN_EMAIL"),
        role=Role.admin,
        password=hashed_password
    )
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
        except DatabaseError as e:
            print(e)


def create_skills():
    skills: List[Skill] = [
        Skill(name="go"),
        Skill(name="python"),
        Skill(name="javascript"),
        Skill(name="typescript"),
        Skill(name="sql"),
    ]
    engine = create_engine(DATABASE_URI)
    with Session(engine) as session:
        try:
            session.add_all(skills)
            session.commit()
        except DatabaseError as e:
            print(e)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="Works with example employers database."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-a", "--create-admin", action="store_true",
                        help="Create administrator user")
    parser.add_argument("-s", "--create-skills", action="store_true",
                        help="Create default set of skills")
    return parser


def main():
    parser = init_argparse()
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.create_admin:
        create_admin()

    if args.create_skills:
        create_skills()


if __name__ == "__main__":
    main()
