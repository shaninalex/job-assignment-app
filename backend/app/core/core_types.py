from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, conint

MAX_PAGE_SIZE = 50


class Pagination(BaseModel, extra="forbid"):
    """Used only for position list to separate different types of query parameters"""

    limit: Optional[int] = Field(Query(10, description="Page size"))
    offset: Optional[int] = Field(Query(0, description="Page number"))


class APIPositionsQueryParams(BaseModel):
    """Global scope of parameters that can be used in API request for querying positions"""

    limit: Optional[conint(le=MAX_PAGE_SIZE)] = Field(
        Query(10, description=f"Page size, maximum allowed is {MAX_PAGE_SIZE}")
    )
    offset: Optional[int] = Field(Query(0, description="Page number"))

    # String fields. Used for "like" SQL operator
    title: Optional[str] = Field(Query(None, description="In position title"))
    description: Optional[str] = Field(Query(None, description="In position description"))
    # TODO: other position fields to filter and search
    # TODO: sort order
