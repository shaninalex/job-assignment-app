import enum
import json
from typing import Any, Dict

import aio_pika

from pkg.settings import logger


class Exchanges(enum.StrEnum):
    """
    Class defining exchange constants for different communication channels.
    """

    ADMIN = "ex.admin_events"
    EMAIL = "ex.email"
    LOG = "ex.log"


class RoutingKeys(enum.StrEnum):
    """
    class RoutingKeys(enum.StrEnum):
    """

    NEW_USER = "new_user"
    NEW_COMPANY = "new_company"
    NEW_COMPANY_MEMBER = "new_company_member"
    COMPLETE_REGISTRATION_SUCCESS = "complete_registration_success"
    CONFIRM_CODE_SENT = "confirm_code_sent"
    USER_LOGIN = "user_login"
    USER_LOGIN_FAILED = "user_login_failed"
    NEW_POSITION = "new_position"


class EventPublisher:
    """
     class EventPublisher:
    Manages connection to RabbitMQ, declaration of exchanges, and publishing events.

    Attributes
    ----------
    rabbitmq_url: str
        URL for connecting to RabbitMQ.
    connection: aio_pika.RobustConnection
        Robust connection to RabbitMQ.
    channel: aio_pika.RobustChannel
        Channel for communication with RabbitMQ.
    exchanges: dict
        Dictionary storing declared exchanges.

    Methods
    -------
    connect():
        Establishes connection to RabbitMQ and creates a channel.
    declare_exchange(exchange_name, exchange_type, durable):
        Declares an exchange if not already declared.
    publish_event(exchange_name, routing_key, event):
        Publishes an event to a specified exchange.
    close():
        Closes the RabbitMQ connection.
    """

    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection: aio_pika.RobustConnection = None
        self.channel: aio_pika.RobustChannel = None
        self.exchanges: Dict[str, aio_pika.Exchange] = {}

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()
            logger.info("Connected to RabbitMQ and channel created.")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: aio_pika.ExchangeType = aio_pika.ExchangeType.FANOUT,
        durable: bool = True,
    ) -> aio_pika.Exchange:
        if exchange_name in self.exchanges:
            logger.debug(f"Exchange '{exchange_name}' already declared.")
            return self.exchanges[exchange_name]

        try:
            exchange = await self.channel.declare_exchange(exchange_name, exchange_type, durable=durable)
            self.exchanges[exchange_name] = exchange
            logger.info(f"Declared exchange '{exchange_name}' of type '{exchange_type.value}'.")
            return exchange
        except Exception as e:
            logger.error(f"Failed to declare exchange '{exchange_name}': {e}")
            raise

    async def publish_event(self, exchange_name: Exchanges, routing_key: RoutingKeys, event: Dict[str, Any]):
        try:
            if exchange_name not in self.exchanges:
                await self.declare_exchange(exchange_name)

            exchange = self.exchanges[exchange_name]
            message_body = json.dumps(event).encode("utf-8")
            message = aio_pika.Message(
                body=message_body, content_type="application/json", delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            await exchange.publish(message, routing_key=routing_key)
            logger.info(f"Published event to exchange '{exchange_name}' with routing key '{routing_key}': {event}")
        except Exception as e:
            logger.error(f"Failed to publish event to exchange '{exchange_name}': {e}")
            raise

    async def close(self):
        try:
            await self.connection.close()
            logger.info("Closed RabbitMQ connection.")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")
            raise
