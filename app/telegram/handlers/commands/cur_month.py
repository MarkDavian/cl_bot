from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import CurSG
from app.core.funcs.get_employees import func_get_employees, func_get_by_id


async def cmd_cur_month(message: types.Message, state: FSMContext):
    await state.finish()
    emps = func_get_employees()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btns = []
    employees_no_birthday = []
    for employee in emps:
        days_to = employee.get_days_to_birth()
        try:
            if days_to < 31:
                if days_to == 0:
                    btns.append(types.InlineKeyboardButton(f"{employee.name} (завтра)", callback_data=employee.id))
                else:
                    btns.append(types.InlineKeyboardButton(f"{employee.name} (через {days_to} дней)", callback_data=employee.id))
        except Exception as e:
            print(e)
            employees_no_birthday.append(employee.name)

    if len(btns) == 0:
        await message.reply(
            'В ближайший месяц ДР не будет',
            reply_markup=keyboard
        )    
        return
    
    for btn in btns:
        keyboard.add(btn)

    await message.reply(
        'Сотрудники, ДР которых будет в ближайший месяц:',
        reply_markup=keyboard
    )
    if len(employees_no_birthday) != 0:
        await message.reply(
            "Есть сотрудники без указанной даты рождения:\n"
            '\n'.join(employees_no_birthday)
        )
    await state.set_state(CurSG.Choose.state)


async def callback_cur(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    emps = func_get_employees()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btns = []
    for employee in emps:
        days_to = employee.get_days_to_birth()
        if days_to < 31:
            if days_to == 0:
                btns.append(types.InlineKeyboardButton(f"{employee.name} (завтра)", callback_data=employee.id))
            else:
                btns.append(types.InlineKeyboardButton(f"{employee.name} (через {days_to} дней)", callback_data=employee.id))

    if len(btns) == 0:
        await callback.message.edit_text(
            'В ближайший месяц ДР не будет',
            reply_markup=keyboard
        )    
        return
    
    for btn in btns:
        keyboard.add(btn)

    await callback.message.edit_text(
        'Сотрудники, ДР которых будет в ближайший месяц:',
        reply_markup=keyboard
    )
    await state.set_state(CurSG.Choose.state)


async def choose_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CurSG.Employee.state)
    emp_id = callback.data
    employee = func_get_by_id(emp_id)

    days_to = employee.get_days_to_birth()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='employees'))

    text_dr = f'<b>ДР через (дней):</b> {days_to}'
    if days_to == 0:
        text_dr = 'Завтра день рождения!'

    await callback.message.edit_text(
        f'<b>ФИО сотрудника:</b> {employee.name}\n'
        f'<b>Дата рождения:</b> {employee.birthday}\n'
        f'<b>Полных лет:</b> {employee.get_years_old()}\n'
        f'<b>ID:</b> {employee.id}\n\n'
        f'{text_dr}',
        reply_markup=keyboard
    )



def reg_cur_month_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_cur_month, commands='current_month', state='*')
    dp.register_callback_query_handler(callback_cur, state=CurSG.Employee)

    dp.register_callback_query_handler(choose_emp, state=CurSG.Choose)