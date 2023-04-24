from bot.db import User
from bot.entities.base_manager import BaseManager


class UserManager(BaseManager):
    model = User
