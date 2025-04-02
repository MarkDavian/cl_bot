"""
Модуль общих обработчиков команд Telegram-бота.

Этот модуль содержит обработчики для общих команд и действий,
которые доступны во всех состояниях бота, таких как отмена
текущей операции. Предоставляет функции для регистрации этих
обработчиков в диспетчере сообщений.
"""

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def __cancel(message: types.Message, state: FSMContext):
    """
    Внутренний метод для отмены текущей операции.
    
    Сбрасывает текущее состояние и отправляет сообщение пользователю
    о том, что действие было отменено.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
        state (FSMContext): Контекст состояния пользователя
    """
    await state.finish()

    await message.reply(
        'Действие отменено',
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Обработчик команды /cancel для отмены текущей операции.
    
    Вызывается при отправке пользователем команды /cancel.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
        state (FSMContext): Контекст состояния пользователя
    """
    await __cancel(message, state)


async def reply_cancel(message: types.Message, state: FSMContext):
    """
    Обработчик текстового сообщения "отменить" для отмены текущей операции.
    
    Вызывается при отправке пользователем текста "отменить".
    
    Args:
        message (types.Message): Объект сообщения от пользователя
        state (FSMContext): Контекст состояния пользователя
    """
    await __cancel(message, state)


async def callback_cancel(message: types.Message, state: FSMContext):
    """
    Обработчик callback-запроса для отмены текущей операции.
    
    Вызывается при нажатии на кнопку с callback-данными 'BREAK'.
    Редактирует исходное сообщение вместо отправки нового.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
        state (FSMContext): Контекст состояния пользователя
    """
    await state.finish()

    await message.edit_text(
        'Действие отменено',
        reply_markup=types.ReplyKeyboardRemove()
    )


def reg_cancel_cmd(dp: Dispatcher):
    """
    Регистрирует обработчики команд отмены в диспетчере.
    
    Эта функция должна быть вызвана при инициализации бота
    для регистрации всех обработчиков отмены операций.
    
    Args:
        dp (Dispatcher): Диспетчер сообщений Telegram-бота
    """
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(reply_cancel, Text('отменить', ignore_case=True), state='*')
    dp.register_callback_query_handler(callback_cancel, lambda callback: callback.data == 'BREAK', state='*')