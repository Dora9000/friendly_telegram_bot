import json
import logging

from bot.db.base import create_async_database
from bot.queue.consumer import StatusConsumer
from bot.queue.settings import RabbitmqData
from bot.queue.storage import StatusStorage


async def on_message(service: StatusConsumer, message, async_session, bot) -> None:
    body = json.loads(message.body)
    message_id = body.pop("message_id")
    logging.info(f"Received message with message_id={message_id}")
    await service.react_message(message=body, async_session=async_session, bot=bot)
    logging.info(f"Message with message_id={message_id} has been processed")

    await message.ack()
    logging.info(f"Message with message_id={message_id} was confirmed")


async def run_queue(bot) -> None:
    async_session = await create_async_database()

    connection = await StatusStorage().connection()

    service = StatusConsumer()

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(RabbitmqData.status.default_queue)

        async with queue.iterator(no_ack=False) as queue_iter:
            async for message in queue_iter:
                await on_message(
                    service=service,
                    message=message,
                    async_session=async_session,
                    bot=bot,
                )
