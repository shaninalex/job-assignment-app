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

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model: T = model
        self.session = session

    async def get_by_id(self, entity_id) -> Optional[T]:
        result = await self.session.get(self.model, entity_id)
        return result

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()  # Flush to send changes to DB without committing
        await self.session.refresh(obj)
        return obj

    async def update_by_id(self, user_id, obj_in: dict) -> Optional[T]:
        await self.session.execute(update(self.model).where(self.model.id == user_id).values(**obj_in))
        return await self.get_by_id(user_id)

    async def delete_by_id(self, user_id) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == user_id))
