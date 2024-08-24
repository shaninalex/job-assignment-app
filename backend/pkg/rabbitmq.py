import pika
import json
from pika.adapters.blocking_connection import BlockingChannel
from sqlalchemy.ext.asyncio import AsyncSession
from database import (
    CompanyManager,
    Company,
    User,
    ConfirmCode,
    ConfirmStatusCode,
)
from pkg import utils


def create_new_candidate(channel: BlockingChannel, user: User):
    d = {"user": user.json()}
    channel.basic_publish(
        "ex.admin_events",
        "new_user",
        json.dumps(d),
        pika.BasicProperties(
            content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
        ),
    )


async def confirm_account(
    session: AsyncSession, channel: BlockingChannel, user: User, code: ConfirmCode
):
    async with session:
        d = {
            "name": user.name,
            "email": user.email,
            "code": code.code,
            "code_id": str(code.id),
        }
        channel.basic_publish(
            "ex.email",
            "confirm_registration",
            json.dumps(d),
            pika.BasicProperties(
                content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
            ),
        )


def create_new_company(
    channel: BlockingChannel, company: Company, member: CompanyManager, user: User
):
    d = {
        "company": company.json(),
        "user": user.json(),
        "member": member.json(),
    }
    channel.basic_publish(
        "ex.admin_events",
        "new_company",
        json.dumps(d),
        pika.BasicProperties(
            content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
        ),
    )
