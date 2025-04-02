from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.funcs.user import get_user, save_user

from app.telegram.handlers.commands.settings.states import SettingsSG

from .common import __main_settings_msg


async def reply_notify_me(message: types.Message, state: FSMContext):
    user = get_user(message)

    if user.chat_notify == False:
        user.chat_notify = True
        save_user(user)

    await message.reply(
            "Настройка уведомлений включена"
        )
    
    await message.bot.send_message(
        message.from_user.id,
        __main_settings_msg(user),
        parse_mode='html'
    )


async def reply_not_notify_me(message: types.Message, state: FSMContext):
    user = get_user(message)

    if user.chat_notify == True:
        user.chat_notify = False
        save_user(user)
    
    await message.reply(
            "Настройка уведомлений отключена"
        )

    await message.bot.send_message(
        message.from_user.id,
        __main_settings_msg(user),
        parse_mode='html'
    )


def reg_settings_notify(dp: Dispatcher):
    dp.register_message_handler(reply_notify_me, Text(equals='присылать уведомления мне в чат', ignore_case=True), state=SettingsSG.start.state)
    dp.register_message_handler(reply_not_notify_me, Text(equals='не присылать уведомления мне в чат', ignore_case=True), state=SettingsSG.start.state)