import json
import uuid

from aio_pika import Message

from bot.queue.settings import RabbitmqData
from bot.queue.storage import GenerationStorage
from bot.utils import Singleton


class GenerationProducer(metaclass=Singleton):
    def __init__(self) -> None:
        self.storage = None
        self.default_routing_key = RabbitmqData.generation.default_queue

    def _data_wrapper(self, data: dict) -> dict:
        init_k = data.pop("init_k")
        grad_k = data.pop("grad_k")

        return {
            **data,
            "message_id": uuid.uuid4().hex,
            "init_k": str(init_k),
            "grad_k": str(grad_k),
        }

    async def send(self, data: dict) -> None:
        message = json.dumps(self._data_wrapper(data)).encode("utf-8")

        if not self.storage:
            connection = await GenerationStorage().connection()
            self.storage = await connection.channel()
            await self.storage.declare_queue(self.default_routing_key)

        await self.storage.default_exchange.publish(
            Message(body=message), routing_key=self.default_routing_key
        )
