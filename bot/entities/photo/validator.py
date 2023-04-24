from bot.entities.base_validator import BaseValidator
from bot.exceptions import NoCaptionException


class PhotoValidator(BaseValidator):
    def validate_caption(self, caption: str) -> None:
        if not caption:
            raise NoCaptionException()
