import logging
from typing import Generic, List, TypeVar, Type, Optional
from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    async def update_by_id(self, session: AsyncSession, entity_id, obj_in: dict) -> Optional[T]:
        await session.execute(update(self.model).where(self.model.id == entity_id).values(**obj_in))
        return await self.get_by_id(session, entity_id)

    async def delete_by_id(self, session: AsyncSession, entity_id) -> None:
        await session.execute(delete(self.model).where(self.model.id == entity_id))

    async def list(self, session: AsyncSession, **kwargs) -> List[T]:
        stmt = select(self.model)
        filters = {}
        limit = None
        offset = None
        for k in kwargs.keys():
            if k == "limit":
                limit = kwargs[k]
            elif k == "offset":
                offset = kwargs[k]
            else:
                filters[k] = kwargs[k]

        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        if len(filters) != 0:
            for key, value in filters.items():
                stmt = stmt.where(getattr(self.model, key) == value)
        result = await session.execute(stmt)
        return result.scalars().all()
