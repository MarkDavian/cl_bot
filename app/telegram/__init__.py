"""
Модуль инициализации Telegram-бота.

Этот модуль содержит функции для запуска и настройки Telegram-бота.
Он отвечает за создание экземпляра бота, диспетчера сообщений,
регистрацию всех обработчиков команд и запуск цикла обработки сообщений.
"""

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import SETTINGS

from app.telegram.handlers.common import reg_cancel_cmd
from app.telegram.handlers.commands import reg_commands


async def start_bot():
    """
    Асинхронная функция запуска Telegram-бота.
    
    Выполняет следующие операции:
    1. Получает токен бота из настроек приложения
    2. Создает экземпляр бота с поддержкой HTML-форматирования
    3. Инициализирует диспетчер сообщений с хранилищем состояний в памяти
    4. Регистрирует обработчики команд отмены и других команд
    5. Запускает цикл опроса серверов Telegram для получения сообщений
    """
    token = SETTINGS.BOT_TOKEN
    bot = Bot(token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    reg_cancel_cmd(dp)
    reg_commands(dp)
    await dp.start_polling()