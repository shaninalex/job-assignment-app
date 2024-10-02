"""
Set of senders for rabbitmq

NOTE: pika will be replaced with aio-pika
https://aio-pika.readthedocs.io/en/latest/quick-start.html
Because pika itself does not support ( or support in not convenient way ) async/await

"""

import enum
import json

import pika
from pika.adapters.blocking_connection import BlockingConnection


class Exchanges(enum.Enum):
    ADMIN = "ex.admin_events"
    EMAIL = "ex.email"


class RoutingKeys(enum.Enum):
    NEW_USER = "new_user"
    NEW_COMPANY = "new_company"
    COMPLETE_REGISTRATION_SUCCESS = "complete_registration_success"
    CONFIRM_CODE_SEND = "send_confirm_code"


properties = pika.BasicProperties(
    content_type="text/json", delivery_mode=pika.DeliveryMode.Transient
)

# into admin exchange


def admin_create_new_candidate(connection: BlockingConnection, user: dict):
    d = {"user": user}
    connection.channel().basic_publish(
        Exchanges.ADMIN.value,
        RoutingKeys.NEW_USER.value,
        json.dumps(d),
        properties,
    )


def admin_create_new_company(
    connection: BlockingConnection, company: dict, member: dict, user: dict
):
    d = {
        "company": company,
        "user": user,
        "member": member,
    }
    connection.channel().basic_publish(
        Exchanges.ADMIN.value,
        RoutingKeys.NEW_COMPANY.value,
        json.dumps(d),
        properties,
    )


def admin_confirm_account_success(connection: BlockingConnection, user: dict):
    d = {"user": user}
    connection.channel().basic_publish(
        Exchanges.ADMIN.value,
        RoutingKeys.COMPLETE_REGISTRATION_SUCCESS.value,
        json.dumps(d),
        properties,
    )


#
# into email exchange
#


def email_confirm_account(connection: BlockingConnection, user: dict, code: dict):
    d = {
        "user": user,
        "code": code,
    }
    connection.channel().basic_publish(
        Exchanges.EMAIL.value,
        RoutingKeys.CONFIRM_CODE_SEND.value,
        json.dumps(d),
        properties,
    )


def email_confirm_account_success(connection: BlockingConnection, user: dict):
    d = {
        "user": user,
    }
    connection.channel().basic_publish(
        Exchanges.EMAIL.value,
        RoutingKeys.COMPLETE_REGISTRATION_SUCCESS.value,
        json.dumps(d),
        properties,
    )
