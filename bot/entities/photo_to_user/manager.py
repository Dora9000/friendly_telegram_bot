from bot.db import PhotoToUser
from bot.entities.base_manager import BaseManager
from bot.entities.photo_to_user.validator import PhotoToUserValidator


class PhotoToUserManager(BaseManager):
    model = PhotoToUser
    validator_model = PhotoToUserValidator
