from .base_manager import BaseManager
from db import User


class UserManager(BaseManager):
    model = User
