from .base_manager import BaseManager
from db import PhotoToUser


class PhotoToUserManager(BaseManager):
    model = PhotoToUser
