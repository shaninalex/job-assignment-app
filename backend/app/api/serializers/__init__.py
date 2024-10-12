"""
This package provide a set of datatypes for in/out transaction in API

Motivation:
It's not correct to return direct objects from database. And Not correct to use them as a payloads for POST/PATCH/PUT 
requests.
"""

from typing import Any, List, Union

from pydantic import BaseModel


class APIResponse(BaseModel):
    data: Union[Any, None] = None
    error: Union[Any, None] = None
    message: List[str] = []
    status: bool = True
