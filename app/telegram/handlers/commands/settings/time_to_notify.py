from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import ALLOWED_TIME_NOTIFY

from app.core.types import NAMED_INTERVALS, App
from app.core.funcs.app import get_app
from app.telegram.handlers.commands.settings.states import SettingsSG

from .cmd_settings import cmd_settings


def _time_notify_menu_msg(app: App):
    notify_time = app.time_to_notify

    return (
            "<b>Текущие настройки времени рассылки:</b>\n"
            f"Время оповещения: <b>{notify_time}</b>\n"
           )


async def reply_time_notify_menu(message: types.Message, state: FSMContext):
    await state.set_state(SettingsSG.time_notify_start.state)
    app = get_app()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Изменить время оповещения'))
    keyboard.add(types.KeyboardButton('Назад'))
    
    await message.reply(
            _time_notify_menu_msg(app),
            parse_mode='html',
            reply_markup=keyboard
    )


async def change_interval(message: types.Message, state: FSMContext):
    await state.set_state(SettingsSG.time_notify_change.state)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Назад'))
    buttons = [types.KeyboardButton(text) for text in list(ALLOWED_TIME_NOTIFY.keys())]
    keyboard.row(*buttons[0:4])
    keyboard.row(*buttons[4:8])
    keyboard.row(*buttons[8:12])
    keyboard.row(*buttons[12:16])

    await message.reply(
        f"<b>Выбери новое время оповещения из списка (в клавиатуре)</b>\n",
        parse_mode='html',
        reply_markup=keyboard
    )


async def time_notify_choosen(message: types.Message, state: FSMContext):
    time_notify = message.text
    if time_notify not in list(ALLOWED_TIME_NOTIFY.keys()):
        await message.reply(
            f'Ты выбрал (или написал) неразрешенный вариант "{time_notify}"\n'
            'Выбери наиболее подходящий из списка ниже'
        )
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))

    await message.reply(
        (
        f"<b>Ты выбрал {time_notify}</b>\n"
        'Включить это время оповещения?'
        ),
        parse_mode='html',
        reply_markup=keyboard
    )
    await state.set_data({'time_notify': time_notify})
    await state.set_state(SettingsSG.accept_time_notify.state)


async def time_notify_accept(message: types.Message, state: FSMContext):
    if message.text.lower() == 'нет':
        await message.reply(
            'Изменение отменено',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()
        return
    
    data = await state.get_data()
    time_notify = data.get('time_notify')

    app = get_app()
    app.time_to_notify = ALLOWED_TIME_NOTIFY[time_notify]
    app.save()
    
    await message.reply(
        f'Время оповещения {time_notify} установлено!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()

    await state.set_state(SettingsSG.time_notify_start.state)
    app = get_app()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Изменить время оповещения"))
    keyboard.add(types.KeyboardButton('Назад'))
    
    await message.reply(
            _time_notify_menu_msg(app),
            parse_mode='html',
            reply_markup=keyboard
    )


def reg_settings_time_notify(dp: Dispatcher):
    dp.register_message_handler(cmd_settings, Text(equals='назад', ignore_case=True), state=SettingsSG.time_notify_start.state)

    dp.register_message_handler(reply_time_notify_menu, Text(equals='время оповещения', ignore_case=True), state=SettingsSG.start.state)

    dp.register_message_handler(change_interval, Text(equals='изменить время оповещения', ignore_case=True), state=SettingsSG.time_notify_start.state)
    dp.register_message_handler(time_notify_choosen, state=SettingsSG.time_notify_change.state)
    dp.register_message_handler(time_notify_accept, state=SettingsSG.accept_time_notify.state)