import pika
from pika.adapters.blocking_connection import BlockingChannel
from sqlalchemy.ext.asyncio import AsyncSession
from database import (
    Candidate,
    CompanyManager,
    Company,
    Auth,
    ConfirmCode,
    ConfirmStatusCode,
)
from pkg import utils


def create_new_candidate(channel: BlockingChannel, candidate: Candidate):
    d = {"candidate": candidate.json()}
    channel.basic_publish(
        "ex.admin_events",
        "candidate",
        str(d),
        pika.BasicProperties(
            content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
        ),
    )


async def confirm_account(
    session: AsyncSession, channel: BlockingChannel, auth: Auth, name: str
):
    async with session:
        confirm_code = ConfirmCode(
            email=auth.email,
            code=utils.generate_code(6),
            status=ConfirmStatusCode.SENDED,
        )
        session.add(confirm_code)
        await session.commit()
        d = {
            "name": name,
            "email": auth.email,
            "code": confirm_code.code,
            "code_id": confirm_code.id,
        }
        channel.basic_publish(
            "ex.email",
            "candidate",
            str(d),
            pika.BasicProperties(
                content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
            ),
        )


def create_new_company(
    channel: BlockingChannel, company: Company, member: CompanyManager
):
    d = {
        "company": company.json(),
        "member": member.json(),
    }
    channel.basic_publish(
        "ex.admin_events",
        "candidate",
        str(d),
        pika.BasicProperties(
            content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
        ),
    )
