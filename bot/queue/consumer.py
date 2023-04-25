class StatusConsumer:
    @classmethod
    async def react_message(cls, message: dict) -> None:
        print("consumer!")
        generation_message_id = message["generation_message_id"]
        percent = message["percent"]
        print(message)
