from bot.entities.base_validator import BaseValidator
from bot.exceptions import ParamFormatException
from bot.exceptions import ParamValueException


class UserValidator(BaseValidator):
    def validate_param(self, text: str, param_name: str) -> float:
        try:
            k = text[len(f"/{param_name}") :].strip()
            k = float(k)
            if k > 0.9 or k < 0.001:
                raise ParamValueException()
        except Exception:
            raise ParamFormatException()

        return k
