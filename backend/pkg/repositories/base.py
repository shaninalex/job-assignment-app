from typing import Generic, TypeVar, Type, Optional

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    BaseRepository responsible for common operations like
    create, get/delete/update by id. List's or query operation
    has infinite amount of variations and options, so implementation
    of list method is a responsibility of concrete model repository.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        result = await self.session.get(self.model, entity_id)
        return result

    async def create(self, obj: T) -> T:
        # obj = self.model(obj_in)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_by_id(self, id: int, obj_in: dict) -> Optional[T]:
        await self.session.execute(update(self.model).where(self.model.id == id).values(**obj_in))
        await self.session.commit()
        return await self.get_by_id(id)

    async def delete_by_id(self, id: int) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == id))
        await self.session.commit()
