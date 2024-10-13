from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.company import APIPosition
from app.api.serializers import APIResponseGen
from app.core.core_types import APIPositionsQueryParams, Pagination
from app.db.operations.position_op import positions_list, PartialPositionSearchPayload
from app.db.session import get_db_session

router = APIRouter(
    tags=["Public"],
    prefix="/api/v1/public",
)


@router.get("/positions")
async def public_list_positions_handler(
    query: APIPositionsQueryParams = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[List[APIPosition]]:
    pagination = Pagination(limit=query.limit, offset=query.offset)
    string_params = PartialPositionSearchPayload(**query.model_dump(exclude_unset=True)).model_dump(exclude_none=True)
    positions = await positions_list(
        session,
        params=None,
        string_params=string_params if len(string_params) else None,
        pagination=pagination,
    )
    api_positions: List[APIPosition] = []
    for p in positions:
        api_positions.append(APIPosition(**p.__dict__))
    return APIResponseGen(data=api_positions)
