from typing import Optional
from pydantic import BaseModel


class Pagination(BaseModel, extra="forbid"):
    limit: Optional[int]
    offset: Optional[int]
