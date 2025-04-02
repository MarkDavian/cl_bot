from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ALLOWED_INTERVALS

from app.core.types import NAMED_INTERVALS, App
from app.core.funcs.app import get_app
from app.core.funcs.correct_date import humanize_date
from app.telegram.handlers.commands.settings.states import SettingsSG


def _intervals_menu_msg(app: App):
    dr = app.dr_notify_time_interval
    lmk = app.lmk_notify_time_interval
    anniv = app.anniversary_time_interval
    certs = app.certs_time_interval

    return (
            "<b>Текущие настройки интервалов рассылки:</b>\n\n"
            f"<b>ДР:</b> {humanize_date(dr)}\n"
            f"<b>ЛМК:</b> {humanize_date(lmk)}\n"
            f"<b>ЮБИЛЕЙ:</b> {humanize_date(anniv)}\n"
            f"<b>СЕРТИФИКАТЫ:</b> {humanize_date(certs)}\n"
           )


async def reply_intervals_menu(message: types.Message, state: FSMContext):
    await state.set_state(SettingsSG.intervals_start.state)
    app = get_app()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.dr.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.lmk.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.anniversary.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.certs.button_txt))
    keyboard.add(types.KeyboardButton('Назад'))
    
    await message.reply(
            _intervals_menu_msg(app),
            parse_mode='html',
            reply_markup=keyboard
    )


async def change_time(message: types.Message, state: FSMContext):
    await state.set_state(SettingsSG.time_start.state)



async def change_interval(message: types.Message, state: FSMContext):
    current = NAMED_INTERVALS.get_type(message.text)
    await state.update_data(current_interval=current.type)

    await state.set_state(SettingsSG.change_interval.state)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Назад'))
    keyboard.add(*[types.KeyboardButton(text) for text in list(ALLOWED_INTERVALS.keys())])

    await message.reply(
        f"<b>Выбери новый интервал (для {current.type}) из списка (в клавиатуре)</b>\n",
        parse_mode='html',
        reply_markup=keyboard
    )


async def interval_choosen(message: types.Message, state: FSMContext):
    interval = message.text
    if interval not in list(ALLOWED_INTERVALS.keys()):
        await message.reply(
            f'Ты выбрал неразрешенный интервал "{interval}"\n'
            'Выбери наиболее подходящий из списка ниже'
        )
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))

    await message.reply(
        (
        f"<b>Ты выбрал {interval}</b>\n"
        'Включить этот интервал?'
        ),
        parse_mode='html',
        reply_markup=keyboard
    )
    await state.update_data(choosen_interval=interval)
    await state.set_state(SettingsSG.accept_interval.state)


async def interval_accept(message: types.Message, state: FSMContext):
    if message.text.lower() == 'нет':
        await message.reply(
            'Изменение отменено',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()
        return
    
    data = await state.get_data()
    current_interval = data.get('current_interval')
    interval = data.get('choosen_interval')

    app = get_app()
    try:
        if current_interval == NAMED_INTERVALS.lmk.type:
            app.lmk_notify_time_interval = ALLOWED_INTERVALS[interval]
        elif current_interval == NAMED_INTERVALS.dr.type:
            app.dr_notify_time_interval = ALLOWED_INTERVALS[interval]
        elif current_interval == NAMED_INTERVALS.anniversary.type:
            app.anniversary_time_interval = ALLOWED_INTERVALS[interval]
        elif current_interval == NAMED_INTERVALS.certs.type:
            app.certs_time_interval = ALLOWED_INTERVALS[interval]
        else:
            await message.reply('Нет обработчика типа Interval класса ChangeableIntervals')
            return
    except Exception as e:
        print(e)
        await message.reply(f'Что-то пошло не так ({e})')
        return
    
    app.save()
    
    await message.reply(
        f'Интервал {interval} установлен!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()

    await state.set_state(SettingsSG.intervals_start.state)
    app = get_app()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.dr.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.lmk.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.anniversary.button_txt))
    keyboard.add(types.KeyboardButton(NAMED_INTERVALS.certs.button_txt))
    keyboard.add(types.KeyboardButton('Назад'))
    
    await message.reply(
            _intervals_menu_msg(app),
            parse_mode='html',
            reply_markup=keyboard
    )
