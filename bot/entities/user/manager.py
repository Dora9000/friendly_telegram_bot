from aiogram.types import Message

from bot.db import User
from bot.entities.base_manager import BaseManager
from bot.entities.user.validator import UserValidator


class UserManager(BaseManager):
    model = User
    validator_model = UserValidator

    async def get_or_create_user(self, message: Message) -> User:
        user = await self.queries.get_entity(filters={"id": message.from_user.id})

        if not user:
            user = await self.queries.create(
                entity=User(
                    id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                )
            )
        return user

    async def update_param(self, message: Message, param_name: str) -> None:
        user = await self.get_or_create_user(message)
        k = self.validator.validate_param(text=message.text, param_name=param_name)
        await self.queries.update(filters={"id": user.id}, values={param_name: k})
