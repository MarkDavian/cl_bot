from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import AddSG
from app.core.funcs.add_employee import func_add_employee
from app.core.funcs.correct_date import date_incorrect


async def cmd_add(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(
        'Напиши ФИО сотрудника:'
    )
    await state.set_state(AddSG.start.state)


# start state
async def add_fio(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            'name': name,
            'birthday': 'Не указано',
            'workstarted': 'Не указано',
            'lmk': 'Не указано'
        }
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Пропустить'))

    await message.reply(
        f'<b>ФИО сотрудника:</b> {name}\n\n'
        'Напиши дату его рождения, вот так: 31.10.2003',
        reply_markup=keyboard
    )
    await state.set_state(AddSG.birthday.state)


# birthday state
async def add_birthday(message: types.Message, state: FSMContext):
    if message.text.lower() != 'пропустить':
        birthday = message.text
        incorrect = date_incorrect(birthday)
        if incorrect:
            await message.reply(
                f"{incorrect}"
                "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
            )
            return
        await state.update_data({'birthday': birthday})

    data = await state.get_data()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Пропустить'))
    await message.reply(
        f'<b>ФИО сотрудника:</b> {data["name"]}\n'
        f'<b>Дата рождения:</b> {data["birthday"]}\n\n'
        'Напиши дату начала работы:',
        reply_markup=keyboard
    )
    await state.set_state(AddSG.workstarted.state)


# workstarted state
async def add_workstarted(message: types.Message, state: FSMContext):
    if message.text.lower() != 'пропустить':
        workstarted = message.text
        incorrect = date_incorrect(workstarted)
        if incorrect:
            await message.reply(
                f"{incorrect}"
                "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
            )
            return
        await state.update_data({'workstarted': workstarted})

    data = await state.get_data()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Пропустить'))
    await message.reply(
        f'<b>ФИО сотрудника:</b> {data["name"]}\n'
        f'<b>Дата рождения:</b> {data["birthday"]}\n'
        f'<b>Начало работы:</b> {data["workstarted"]}\n\n'
        'Напиши дату получения Личной Медицинской Книжки:',
        reply_markup=keyboard
    )
    await state.set_state(AddSG.lmk.state)


# lmk state
async def add_lmk(message: types.Message, state: FSMContext):
    if message.text.lower() != 'пропустить':
        lmk = message.text
        incorrect = date_incorrect(lmk)
        if incorrect:
            await message.reply(
                f"{incorrect}"
                "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
            )
            return
        await state.update_data({'lmk': lmk})

    data = await state.get_data()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Да'))
    keyboard.add(types.KeyboardButton('Нет'))
    await message.reply(
        f'<b>ФИО сотрудника:</b> {data["name"]}\n'
        f'<b>Дата рождения:</b> {data["birthday"]}\n'
        f'<b>Начало работы:</b> {data["workstarted"]}\n'
        f'<b>ЛМК от:</b> {data["lmk"]}\n\n'
        '<b>Все верно?</b>',
        reply_markup=keyboard
    )
    await state.set_state(AddSG.end.state)


# end state
async def add_emp(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    birthday = data['birthday']
    workstarted = data['workstarted']
    lmk = data['lmk']
    registration = datetime.now().strftime('%d.%m.%Y')

    func_add_employee(
        name,
        birthday,
        registration,
        workstarted,
        lmk
    )

    await message.reply(
        f'<b>ФИО сотрудника:</b> {name}\n'
        f'<b>Дата рождения:</b> {birthday}\n'
        f'<b>Начало работы:</b> {workstarted}\n'
        f'<b>ЛМК от:</b> {lmk}\n\n'
        f'<b>СОТРУДНИК ДОБАВЛЕН!</b>',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()


def reg_add_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_add, commands='add', state='*')

    dp.register_message_handler(add_emp, Text('да', ignore_case=True), state=AddSG.end)
    dp.register_message_handler(cmd_add, Text('нет', ignore_case=True), state=AddSG.end)

    dp.register_message_handler(add_fio, state=AddSG.start)
    dp.register_message_handler(add_birthday, state=AddSG.birthday)
    dp.register_message_handler(add_workstarted, state=AddSG.workstarted)
    dp.register_message_handler(add_lmk, state=AddSG.lmk)

    # dp.register_message_handler(cmd_menu, Text('назад', ignore_case=True), state=LastDateSG.start)
