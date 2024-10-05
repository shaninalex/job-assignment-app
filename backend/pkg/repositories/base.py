from typing import Generic, TypeVar, Type, Optional

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    BaseRepository class to handle CRUD operations for a given model.

    Parameters
    ----------
    model : Type[T]
        The SQLAlchemy model type to be handled by this repository.
    session : AsyncSession
        The SQLAlchemy asynchronous session instance.
    """

    def __init__(self, model: Type[T]):
        self.model: T = model

    async def get_by_id(self, session: AsyncSession, entity_id) -> Optional[T]:
        result = await session.get(self.model, entity_id)
        return result

    async def create(self, session: AsyncSession, obj: T) -> T:
        session.add(obj)
        await session.flush()  # Flush to send changes to DB without committing
        await session.refresh(obj)
        return obj

    async def update_by_id(self, session: AsyncSession, user_id, obj_in: dict) -> Optional[T]:
        await session.execute(update(self.model).where(self.model.id == user_id).values(**obj_in))
        return await self.get_by_id(session, user_id)

    async def delete_by_id(self, session: AsyncSession, user_id) -> None:
        await session.execute(delete(self.model).where(self.model.id == user_id))
