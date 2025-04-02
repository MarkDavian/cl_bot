from aiogram import types
from aiogram.dispatcher import FSMContext

from app.core.funcs.user import get_user

from app.telegram.handlers.commands.settings.states import SettingsSG

from .common import __main_settings_msg


async def cmd_settings(message: types.Message, state: FSMContext):
    await state.finish()
    user = get_user(message)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton("Присылать уведомления мне в чат"))
    keyboard.add(types.InlineKeyboardButton("Не присылать уведомления мне в чат"))
    keyboard.add(types.InlineKeyboardButton("Интервалы сообщений"))
    keyboard.add(types.InlineKeyboardButton("Время оповещения"))
    keyboard.add(types.InlineKeyboardButton("Сменить пароль бота"))

    await message.reply(
        __main_settings_msg(user),
        parse_mode='html',
        reply_markup=keyboard
        
    )
    await state.set_state(SettingsSG.start.state)





