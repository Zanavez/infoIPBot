from aiogram import types, Router
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")