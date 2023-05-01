from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.entities.user.manager import UserManager

router = Router()


@router.message(Command(commands=["init_k"]))
async def command_init_k_handler(message: Message, session: AsyncSession) -> None:
    await UserManager(session).update_param(message=message, param_name="init_k")
    await message.answer(f"init K was updated")


@router.message(Command(commands=["grad_k"]))
async def command_grad_k_handler(message: Message, session: AsyncSession) -> None:
    await UserManager(session).update_param(message=message, param_name="grad_k")
    await message.answer(f"grad K was updated")
