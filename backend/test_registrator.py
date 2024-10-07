import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from pkg.consts import Role
from pkg.services.common.new_registrator import CandidateRegistration, CompanyRegistration, MemberRegistration, registration_process
from pkg.services.event_service import EventPublisher
from pkg.settings import Config, Redis

config = Config(
    DATABASE_URI="postgresql+asyncpg://postgres:postgres@localhost:5432/application",
    DEBUG=True,
    REDIS=Redis(REDIS_DB=0, REDIS_PORT=6379, REDIS_HOST="localhost"),
    APP_PORT=8080,
    RABBIT_URL="amqp://guest:guest@localhost/",
    APP_SECRET="secret_token_string",
)

async def main():
    eng = create_async_engine(config.DATABASE_URI, echo=False)
    session = AsyncSession(bind=eng, expire_on_commit=False)
    event_publisher = EventPublisher(rabbitmq_url=config.RABBIT_URL)
    await event_publisher.connect()

    company_registration: CompanyRegistration = CompanyRegistration(
        company_name="ABC",
        company_website="https://www.abc.com",
        company_email="abc@email.com",
        name="Jeff Besos",
        email="jeff@besos.abc.com",
        password="123",
        password_confirm="123",
    )
    await registration_process(
        type_=Role.COMPANY_ADMIN,
        data=company_registration.model_dump(),
        publisher=event_publisher,
        session=session,
    )

    member: MemberRegistration = MemberRegistration(
        # hardcoded because it's proof of concept
        # real company id will be taken from request context
        company_id="fea7cbd2-5585-4990-82a8-270f6fc415a3", 
        registrator_user_id=str(uuid.uuid4()),
        name="ABC member",
        email="scully@xfiles.com",
        password="123",
        password_confirm="123",
    )
    await registration_process(
        type_=Role.COMPANY_MEMBER,
        data=member.model_dump(),
        publisher=event_publisher,
        session=session,
    )

    candidate: CandidateRegistration = CandidateRegistration(
        name="Mulder",
        email="mulder@xfiles.com",
        password="123",
        password_confirm="123",
    )
    await registration_process(
        type_=Role.CANDIDATE,
        data=candidate.model_dump(),
        publisher=event_publisher,
        session=session,
    )


if __name__ == "__main__":
    asyncio.run(main())
