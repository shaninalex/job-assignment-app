import logging

from app.db import users
from app.models import AdminCreateUserPayload


class UserRepository:
    def __init__(self, db_connection):
        self.conn = db_connection

    def login():
        ...

    def create(self,
               payload: AdminCreateUserPayload,
               admin: bool = False) -> bool:
        print(payload)
        return True
