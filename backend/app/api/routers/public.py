from typing import List
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers.company import APICompany, APIPosition
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
        api_positions.append(APIPosition(
            id=p.id,
            title=p.title,
            description=p.description,
            responsibilities=p.responsibilities,
            requirements=p.requirements,
            interview_stages=p.interview_stages,
            offer=p.offer,
            company_id=p.company_id,
            remote=p.remote,
            salary=p.salary,
            hours=p.hours,
            travel=p.travel,
            status=p.status,
            price_range=p.price_range,
            created_at=p.created_at,
            updated_at=p.updated_at,
            company=APICompany(**p.company.__dict__),
        ))
    return APIResponseGen(data=api_positions)
