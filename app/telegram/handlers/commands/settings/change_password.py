from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.core.funcs.app import change_password
from app.telegram.handlers.commands.settings.states import SettingsSG


async def reply_change_password(message: types.Message, state: FSMContext):
    await state.finish()

    reply_keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
        ).add(
            types.KeyboardButton('Отменить')
            )

    await message.reply(
            "Напиши новый пароль для входа в Бот",
            reply_markup=reply_keyboard
        )
    
    await state.set_state(SettingsSG.change_password_start.state)


async def reply_step_change_password(message: types.Message, state: FSMContext):
    text = message.text
    password = change_password(text)

    await message.reply(
            f"Пароль изменен на: <b>{password}</b>",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    await state.finish()


def reg_settings_change_password(dp: Dispatcher):
    dp.register_message_handler(reply_change_password, Text(equals='сменить пароль бота', ignore_case=True), state=SettingsSG.start.state)
    dp.register_message_handler(reply_step_change_password, state=SettingsSG.change_password_start.state)