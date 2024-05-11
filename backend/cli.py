# Cli for backend

# Usage:
#   python cli.py --create-admin
#   python cli.py --help
import sys
import os
import argparse
from sqlalchemy import create_engine, text

from app.settings import DATABASE_URI
from app.pkg import password


def create_admin():
    engine = create_engine(DATABASE_URI)
    insert = text("""
        INSERT INTO public.users (email, password) VALUES (:email, :password)
    """)
    connection = engine.connect()
    hashed_password = password.get_hashed_password(os.getenv("ADMIN_PASSWORD"))
    connection.execute(
        insert,
        email=os.getenv("ADMIN_EMAIL"),
        password=hashed_password
    )


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="Works with example employers database."
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-a", "--create-admin", action="store_true")
    return parser


def main():
    parser = init_argparse()
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    if args.create_admin:
        create_admin()


if __name__ == "__main__":
    main()
