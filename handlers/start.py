from aiogram import Bot,  Router, F
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize


router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")
