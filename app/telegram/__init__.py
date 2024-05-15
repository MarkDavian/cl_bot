from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import settings

from app.telegram.handlers.common import reg_cancel_cmd
from app.telegram.handlers.commands import reg_commands


async def start_bot():
    token = settings.bot_token
    bot = Bot(token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    reg_cancel_cmd(dp)
    reg_commands(dp)
    await dp.start_polling()