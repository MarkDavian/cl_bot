from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import EmployeesSG
from app.core.funcs.get_employees import func_get_employees, func_get_by_id
from app.core.funcs.correct_date import is_date_correct
from app.core.funcs.add_employee import func_add_employee
from app.core.funcs.del_employee import func_del_emp
from app.core.types.types import EmployeeBuilder


async def cmd_emps(message: types.Message, state: FSMContext):
    await state.finish()
    emps = func_get_employees()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if len(emps) == 0:
        await message.reply(
            'Сотрудников нет',
            reply_markup=keyboard
        )
        return
        
    for employee in emps:
        keyboard.add(types.InlineKeyboardButton(employee.name, callback_data=employee.id))

    await message.reply(
        'Сотрудники:',
        reply_markup=keyboard
    )
    await state.set_state(EmployeesSG.Choose.state)


async def callback_emps(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    emps = func_get_employees()
    await state.update_data({'employees': emps})
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for employee in emps:
        keyboard.add(types.InlineKeyboardButton(employee.name, callback_data=employee.id))

    await callback.message.edit_text(
        'Сотрудники:',
        reply_markup=keyboard
    )
    await state.set_state(EmployeesSG.Choose.state)


async def choose_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Employee.state)
    emp_id = callback.data
    employee = func_get_by_id(emp_id)
    await state.set_data(employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('📋Изменить', callback_data='Change'))
    keyboard.add(types.InlineKeyboardButton('❌Удалить', callback_data='Delete'))
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data='employees'))

    await callback.message.edit_text(
        f'<b>ФИО сотрудника:</b> {employee.name}\n'
        f'<b>Дата рождения:</b> {employee.birthday}\n'
        f'<b>Полных лет:</b> {employee.get_years_old()}\n'
        f'<b>ДР через (дней):</b> {employee.get_days_to()}\n'
        f'<b>Начало работы:</b> {employee.workstarted}\n'
        f'<b>Стаж работы:</b> {employee.get_experience()}\n'
        f'<b>ЛМК от:</b> {employee.lmk}\n\n'
        f'<b>ID:</b> {employee.id}\n'
        f'<b>Дата регистрации:</b> {employee.registration}\n',
        reply_markup=keyboard
    )


async def delete_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Delete.state)
    employee = await state.get_data()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee['id']))
    keyboard.add(types.InlineKeyboardButton('❌УДАЛИТЬ', callback_data='Delete'))

    await callback.message.edit_text(
        f'ФИО сотрудника: {employee["name"]}\n'
        f'<b>ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ УДАЛИТЬ СОТРУДНИКА?</b>',
        reply_markup=keyboard
    )


async def sucker(callback: types.CallbackQuery, state: FSMContext):
    employee = await state.get_data()

    emp = func_del_emp(employee['id'])

    await callback.message.edit_text(
        f'ФИО сотрудника: {emp["name"]}\n'
        f'<b>СОТРУДНИК УДАЛЕН</b>'
    )

    await state.finish()


async def change_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change.state)
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('ФИО сотрудника', callback_data="name"))
    keyboard.add(types.InlineKeyboardButton('Дата рождения', callback_data="birthday"))
    keyboard.add(types.InlineKeyboardButton('Начало работы', callback_data="workstarted"))
    keyboard.add(types.InlineKeyboardButton('ЛМК', callback_data="lmk"))
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'<b>ФИО сотрудника:</b> {employee.name}\n'
        f'<b>Дата рождения:</b> {employee.birthday}\n'
        f'<b>Полных лет:</b> {employee.get_years_old()}\n'
        f'<b>ДР через (дней):</b> {employee.get_days_to()}\n'
        f'<b>Начало работы:</b> {employee.workstarted}\n'
        f'<b>Стаж работы:</b> {employee.get_experience()}\n'
        f'<b>ЛМК от:</b> {employee.lmk}\n\n'
        f'<b>ID:</b> {employee.id}\n'
        f'<b>Дата регистрации:</b> {employee.registration}\n\n'
        f'<b>ЧТО ХОТИТЕ ИЗМЕНИТЬ?</b>',
        reply_markup=keyboard
    )


async def change_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_name.state)
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши ФИО сотрудника',
        reply_markup=keyboard
    )


async def change_name_end(message: types.Message, state: FSMContext):
    name = message.text
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()
    employee.name = name

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новое ФИО сотрудника:\n'
        f'<b>{name}</b>',
        reply_markup=keyboard
    )



async def change_birthday(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_birthday.state)
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату рождения сотрудника',
        reply_markup=keyboard
    )


async def change_birthday_end(message: types.Message, state: FSMContext):
    birthday = message.text
    incorrect = is_date_correct(birthday)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()
    employee.birthday = birthday

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новая дата рождения сотрудника:\n'
        f'<b>{birthday}</b>',
        reply_markup=keyboard
    )


async def change_workstarted(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_workstarted.state)
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату начала работы сотрудника',
        reply_markup=keyboard
    )


async def change_workstarted_end(message: types.Message, state: FSMContext):
    workstarted = message.text
    incorrect = is_date_correct(workstarted)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()
    employee.workstarted = workstarted

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новая дата начала работы сотрудника:\n'
        f'<b>{workstarted}</b>',
        reply_markup=keyboard
    )


async def change_lmk(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_lmk.state)
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату получения ЛМК сотрудника',
        reply_markup=keyboard
    )


async def change_lmk_end(message: types.Message, state: FSMContext):
    lmk = message.text
    incorrect = is_date_correct(lmk)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    employee = await state.get_data()
    employee = EmployeeBuilder(**employee).get_employee()
    employee.lmk = lmk

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новая дата получения ЛМК сотрудника:\n'
        f'<b>{lmk}</b>',
        reply_markup=keyboard
    )


def reg_emp_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_emps, commands='employees', state='*')
    dp.register_callback_query_handler(callback_emps, lambda callback: callback.data == 'employees', state=EmployeesSG.Employee)

    dp.register_callback_query_handler(choose_emp, state=EmployeesSG.Choose)
    dp.register_callback_query_handler(sucker, lambda callback: callback.data == 'Delete', state=EmployeesSG.Delete)
    dp.register_callback_query_handler(choose_emp, state=EmployeesSG.Delete)

    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_name)
    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_birthday)
    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_workstarted)
    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_lmk)

    dp.register_callback_query_handler(delete_emp, lambda callback: callback.data == 'Delete', state=EmployeesSG.Employee)

    dp.register_callback_query_handler(change_emp, lambda callback: callback.data == 'Change', state=EmployeesSG.Employee)

    dp.register_callback_query_handler(change_name, lambda callback: callback.data == 'name', state=EmployeesSG.Change)
    dp.register_message_handler(change_name_end, state=EmployeesSG.Change_name)

    dp.register_callback_query_handler(change_birthday, lambda callback: callback.data == 'birthday', state=EmployeesSG.Change)
    dp.register_message_handler(change_birthday_end, state=EmployeesSG.Change_birthday)

    dp.register_callback_query_handler(change_workstarted, lambda callback: callback.data == 'workstarted', state=EmployeesSG.Change)
    dp.register_message_handler(change_workstarted_end, state=EmployeesSG.Change_workstarted)

    dp.register_callback_query_handler(change_lmk, lambda callback: callback.data == 'lmk', state=EmployeesSG.Change)
    dp.register_message_handler(change_lmk_end, state=EmployeesSG.Change_lmk)

    dp.register_callback_query_handler(choose_emp, state=EmployeesSG.Change)