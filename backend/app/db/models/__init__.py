from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


from .user import User, ConfirmCode  # type: ignore # noqa
from .company import Company  # type: ignore # noqa
from .position import Position  # type: ignore # noqa
