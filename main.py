import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from configs.config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.get_user_ip_number import get_user_ip_number_router
from handlers.start import start_router

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
default = DefaultBotProperties(parse_mode=ParseMode.HTML)

# Диспетчер
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(get_user_ip_number_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())