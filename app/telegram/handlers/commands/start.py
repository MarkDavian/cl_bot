from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from app.core.funcs.app import get_password
from app.core.funcs.user import add_user


class StartSG(StatesGroup):
    start = State()
    dates_diff = State()
    days_for = State()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(StartSG.start.state)

    await message.reply(
        "Пароль"
    )


async def start_write_password(message: types.Message, state: FSMContext):
    password = message.text
    if password != get_password():
        return
    else:
        await message.bot.send_message(
            message.chat.id,
            'Пароль принят, посылаю инструкцию'
        )
        await message.reply_document(
            open('files/Презентация бота.pdf', 'rb'),
            "Привет! Ознакомься с инструкцией)"
        )
        add_user(message.from_user.id, False, datetime.now().strftime('%d.%m.%Y'))
        await state.finish()


def reg_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(start_write_password, state=StartSG.start.state)