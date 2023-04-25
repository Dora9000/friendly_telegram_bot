import asyncio
import json
import logging

from bot.queue.consumer import StatusConsumer
from bot.queue.settings import RabbitmqData
from bot.queue.storage import StatusStorage


async def on_message(service: StatusConsumer, message) -> None:
    body = json.loads(message.body)
    print(body)
    message_id = body.pop("message_id")
    logging.info(f"Received message with message_id={message_id}")
    await service.react_message(message=body)
    logging.info(f"Message with message_id={message_id} has been processed")

    await message.ack()
    logging.info(f"Message with message_id={message_id} was confirmed")


async def main() -> None:
    connection = await StatusStorage().connection()

    service = StatusConsumer()

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(RabbitmqData.status.default_queue)

        async with queue.iterator(no_ack=False) as queue_iter:
            async for message in queue_iter:
                await on_message(service=service, message=message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
