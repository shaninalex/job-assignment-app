import asyncio
import logging

import pika


async def start_background_tasks(app):
    """
    Function to start all necessary background tasks when the app starts.
    """
    logging.info("RabbitMQ: Reconection bg task")
    app["rabbitmq_check"] = asyncio.create_task(check_rabbitmq_connection(app))


async def cancel_background_tasks(app):
    """
    Cancel all running background tasks when the app shuts down.
    """
    logging.info("Cancelling background tasks.")
    task = app["rabbitmq_check"]
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logging.info("Background task cancelled.")


async def check_rabbitmq_connection(app):
    """
    Background task to check and reconnect to RabbitMQ if the connection is lost.
    """
    while True:
        try:
            if app["mq"] is None or not app["mq"].is_open:
                logging.warning("RabbitMQ connection lost. Reconnecting...")
                await connect_rabbitmq(app)
        except Exception as e:
            logging.error(f"Error checking RabbitMQ connection: {e}")

        await asyncio.sleep(5)


async def connect_rabbitmq(app):
    """
    Reconnect to RabbitMQ and store the new connection in the app context.
    """
    # TODO: use os.getenv credential and host variables
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "localhost", credentials=pika.PlainCredentials("guest", "guest")
            )
        )
        app["mq"] = connection
        logging.info("Reconnected to RabbitMQ.")
    except Exception as e:
        logging.error(f"Failed to reconnect to RabbitMQ: {e}")


async def close_rmq_connection(app):
    """
    Close the RabbitMQ connection on shutdown.
    """
    try:
        if app["mq"] and app["mq"].is_open:
            app["mq"].close()
            logging.info("RabbitMQ connection closed.")
    except Exception as e:
        logging.error(f"Error closing RabbitMQ connection: {e}")
