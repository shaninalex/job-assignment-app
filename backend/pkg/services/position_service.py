from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.company.form import PositionForm
from pkg.consts import SalaryType
from pkg.models.models import Position
from pkg.repositories.position_repository import PositionRepository
from pkg.services.event_service import EventPublisher, Exchanges, RoutingKeys


class PositionService:
    def __init__(
        self,
        repository: PositionRepository,
        event_service: EventPublisher,
    ) -> None:
        self.repository = repository
        self.event_service: EventPublisher = event_service

    async def create_new_position(self, session: AsyncSession, payload: PositionForm) -> Position:
        print(payload)
        p = Position(
            title=payload.title,
            description=payload.description,
            responsibilities=payload.responsibilities,
            requirements=payload.requirements,
            interview_stages=payload.interview_stages,
            offer=payload.offer,
            price_range=payload.price_range,
            remote=payload.remote,
            salary=SalaryType(payload.salary),
            hours=payload.hours,
            travel=payload.travel,
            status=payload.status,
            company_id=payload.company_id,
        )
        position = await self.repository.create(session, p)
        if not position:
            raise Exception("unable to create position")
        await self.event_service.publish_event(Exchanges.ADMIN, RoutingKeys.NEW_POSITION, {"position": position.json()})
        return position

    async def list(self, session: AsyncSession) -> Sequence[Position]:
        return await self.repository.list(session)
