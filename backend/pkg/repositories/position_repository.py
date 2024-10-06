from pkg.models import Position
from pkg.repositories.base import BaseRepository


class PositionRepository(BaseRepository[Position]):
    def __init__(self):
        super().__init__(Position)
