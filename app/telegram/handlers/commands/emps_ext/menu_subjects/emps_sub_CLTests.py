import os
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


from app.telegram.handlers.states import EmployeesSG
from app.core.types import EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees, func_get_by_id
from app.core.funcs.correct_date import date_incorrect
from app.core.funcs.add_employee import func_add_employee
from app.core.funcs.del_employee import func_del_emp
from ...common import EmpCallbackData, CLTestsCallbackData


async def emp_cl_tests(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.CLTests.Menu.state)
    
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    
    current_page = 0
    if callback.data.startswith(CLTestsCallbackData.prefix):
        current_page = CLTestsCallbackData.unpack(callback.data).page
        if not current_page:
            current_page = 0

    # Разбиваем тесты на страницы по 4 штуки
    tests_per_page = 4
    total_pages = (len(employee.test_results) + tests_per_page - 1) // tests_per_page
    start_idx = int(current_page) * tests_per_page
    end_idx = min(start_idx + tests_per_page, len(employee.test_results))
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(types.InlineKeyboardButton(
        "Добавить тест",
        callback_data=CLTestsCallbackData(
            action="add_test",
            test_id="",
            page=current_page
        ).pack()
    ))
    
    # Добавляем кнопки тестов для текущей страницы
    for test in employee.test_results[start_idx:end_idx]:
        keyboard.add(types.InlineKeyboardButton(
            f"{test.date} - {test.type}",
            callback_data=CLTestsCallbackData(
                action="view_test",
                test_id=test._id,
                page=current_page
            ).pack()
        ))
    
    # Добавляем навигационные кнопки, если есть больше одной страницы
    nav_buttons = []
    if total_pages > 1:
        if int(current_page) > 0:
            nav_buttons.append(types.InlineKeyboardButton(
                "⬅️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=int(current_page) - 1
                ).pack()
            ))
        if int(current_page) < total_pages - 1:
            nav_buttons.append(types.InlineKeyboardButton(
                "➡️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=int(current_page) + 1
                ).pack()
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
    
    # Добавляем кнопку "Назад"
    keyboard.add(types.InlineKeyboardButton(
        "Назад",
        callback_data=f'back:{employee.id}'
    ))
    
    await callback.message.edit_text(
        f'📊 Срезы знаний сотрудника {employee.name}:\n'
        f'Всего тестов: {len(employee.test_results)}\n'
        f'Страница {int(current_page) + 1} из {total_pages}',
        reply_markup=keyboard
    )


async def view_test_details(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.CLTests.Details.state)
    
    callback_data = CLTestsCallbackData.unpack(callback.data)
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    
    # Находим нужный тест
    test = next((t for t in employee.test_results if t._id == callback_data.test_id), None)
    
    if not test:
        await callback.message.edit_text("Тест не найден")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Назад к списку тестов",
        callback_data=CLTestsCallbackData(
            action="back_to_tests",
            test_id="",
            page=callback_data.page
        ).pack()
    ))
    
    await callback.message.edit_text(
        f'📊 Результаты теста от {test.date}\n\n'
        f'⏱ Время прохождения: {test.completion_time}\n'
        f'🎯 Количество баллов: {test.score}\n'
        f'🏆 Место в списке: {test.rank}',
        reply_markup=keyboard
    )


async def back_to_tests(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.CLTests.Menu.state)
    
    callback_data = CLTestsCallbackData.unpack(callback.data)
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    
    # Разбиваем тесты на страницы по 4 штуки
    tests_per_page = 4
    total_pages = (len(employee.test_results) + tests_per_page - 1) // tests_per_page
    start_idx = int(callback_data.page) * tests_per_page
    end_idx = min(start_idx + tests_per_page, len(employee.test_results))
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    keyboard.add(types.InlineKeyboardButton(
        "Добавить тест",
        callback_data=CLTestsCallbackData(
            action="add_test",
            test_id="",
            page=callback_data.page
        ).pack()
    ))
    
    # Добавляем кнопки тестов для текущей страницы
    for test in employee.test_results[start_idx:end_idx]:
        keyboard.add(types.InlineKeyboardButton(
            f"{test.date} - {test.type}",
            callback_data=CLTestsCallbackData(
                action="view_test",
                test_id=test._id,
                page=callback_data.page
            ).pack()
        ))
    
    # Добавляем навигационные кнопки, если есть больше одной страницы
    nav_buttons = []
    if total_pages > 1:
        if int(callback_data.page) > 0:
            nav_buttons.append(types.InlineKeyboardButton(
                "⬅️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=int(callback_data.page) - 1
                ).pack()
            ))
        if int(callback_data.page) < total_pages - 1:
            nav_buttons.append(types.InlineKeyboardButton(
                "➡️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=int(callback_data.page) + 1
                ).pack()
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
    
    # Добавляем кнопку "Назад"
    keyboard.add(types.InlineKeyboardButton(
        "Назад",
        callback_data=f'back:{employee.id}'
    ))
    
    await callback.message.edit_text(
        f'📊 Срезы знаний сотрудника {employee.name}:\n'
        f'Всего тестов: {len(employee.test_results)}\n'
        f'Страница {int(callback_data.page) + 1} из {total_pages}',
        reply_markup=keyboard
    )

# реагирует на Menu
async def add_test_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.CLTests.Add.Date)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Отмена",
        callback_data=CLTestsCallbackData(
            action="cancel_add",
            test_id="",
            page=0
        ).pack()
    ))
    
    await callback.message.edit_text(
        "📝 Добавление нового теста\n\n"
        "Введите дату теста в формате ДД.ММ.ГГГГ:",
        reply_markup=keyboard
    )

# реагирует на add.date
async def add_test_date(message: types.Message, state: FSMContext):
    if date_incorrect(message.text):
        await message.reply(
            "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 01.01.2024"
        )
        return
    
    await state.update_data(test_date=message.text)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Отмена",
        callback_data=CLTestsCallbackData(
            action="cancel_add",
            test_id="",
            page=0
        ).pack()
    ))
    
    await message.reply(
        "Введите тип теста:",
        reply_markup=keyboard
    )

    await state.set_state(EmployeesSG.CLTests.Add.Type)

# реагирует на add.type
async def add_test_type(message: types.Message, state: FSMContext):
    await state.update_data(test_type=message.text)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Отмена",
        callback_data=CLTestsCallbackData(
            action="cancel_add",
            test_id="",
            page=0
        ).pack()
    ))
    
    await message.reply(
        "Введите время прохождения теста в формате ЧЧ:ММ:",
        reply_markup=keyboard
    )
    await state.set_state(EmployeesSG.CLTests.Add.Time)

# реагирует на add.time
async def add_test_time(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%H:%M")
    except ValueError:
        await message.reply(
            "❌ Неверный формат времени. Используйте формат ЧЧ:ММ\n"
            "Например: 01:30"
        )
        return
    
    await state.update_data(completion_time=message.text)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Отмена",
        callback_data=CLTestsCallbackData(
            action="cancel_add",
            test_id="",
            page=0
        ).pack()
    ))
    
    await message.reply(
        "Введите количество набранных баллов:",
        reply_markup=keyboard
    )
    await state.set_state(EmployeesSG.CLTests.Add.Score)
# реагирует на add.score
async def add_test_score(message: types.Message, state: FSMContext):
    try:
        score = int(message.text)
        if score < 0:
            raise ValueError
    except ValueError:
        await message.reply(
            "❌ Неверный формат баллов. Введите целое положительное число."
        )
        return
    
    await state.update_data(score=score)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Отмена",
        callback_data=CLTestsCallbackData(
            action="cancel_add",
            test_id="",
            page=0
        ).pack()
    ))
    
    await message.reply(
        "Введите место в списке:",
        reply_markup=keyboard
    )
    await state.set_state(EmployeesSG.CLTests.Add.Rank)
# реагирует на add.rank
async def add_test_rank(message: types.Message, state: FSMContext):
    try:
        rank = int(message.text)
        if rank < 1:
            raise ValueError
    except ValueError:
        await message.reply(
            "❌ Неверный формат места. Введите целое положительное число."
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    
    # Создаем новый тест
    from app.core.types import TestResult
    new_test = TestResult(
        date=data['test_date'],
        type=data['test_type'],
        completion_time=data['completion_time'],
        score=data['score'],
        rank=rank
    )
    # Добавляем тест к сотруднику
    employee.add_test_result(new_test)
    # Сохраняем обновленного сотрудника
    await state.reset_data()
    await state.set_data({'employee': employee.__dict__()})

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    # Возвращаемся к списку тестов
    await state.set_state(EmployeesSG.CLTests.Menu.state)
    
    # Разбиваем тесты на страницы по 4 штуки
    tests_per_page = 4
    total_pages = (len(employee.test_results) + tests_per_page - 1) // tests_per_page
    current_page = total_pages - 1  # Переходим на последнюю страницу
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Добавить тест",
        callback_data=CLTestsCallbackData(
            action="add_test",
            test_id="",
            page=current_page
        ).pack()
    ))
    
    # Добавляем кнопки тестов для текущей страницы
    start_idx = current_page * tests_per_page
    end_idx = min(start_idx + tests_per_page, len(employee.test_results))
    
    for test in employee.test_results[start_idx:end_idx]:
        keyboard.add(types.InlineKeyboardButton(
            f"{test.date} - {test.type}",
            callback_data=CLTestsCallbackData(
                action="view_test",
                test_id=test._id,
                page=current_page
            ).pack()
        ))
    
    # Добавляем навигационные кнопки, если есть больше одной страницы
    nav_buttons = []
    if total_pages > 1:
        if current_page > 0:
            nav_buttons.append(types.InlineKeyboardButton(
                "⬅️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=current_page - 1
                ).pack()
            ))
        if current_page < total_pages - 1:
            nav_buttons.append(types.InlineKeyboardButton(
                "➡️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=current_page + 1
                ).pack()
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
    
    # Добавляем кнопку "Назад"
    keyboard.add(types.InlineKeyboardButton(
        "Назад",
        callback_data=employee.id
    ))
    
    await message.reply(
        f'✅ Тест успешно добавлен!\n\n'
        f'📊 Срезы знаний сотрудника {employee.name}:\n'
        f'Всего тестов: {len(employee.test_results)}\n'
        f'Страница {current_page + 1} из {total_pages}',
        reply_markup=keyboard
    )

    await state.set_state(EmployeesSG.CLTests.Menu.state)


async def cancel_add_test(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.CLTests.Menu.state)
    
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    
    # Разбиваем тесты на страницы по 4 штуки
    tests_per_page = 4
    total_pages = (len(employee.test_results) + tests_per_page - 1) // tests_per_page
    current_page = 0
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Добавить тест",
        callback_data=CLTestsCallbackData(
            action="add_test",
            test_id="",
            page=current_page
        ).pack()
    ))
    
    # Добавляем кнопки тестов для текущей страницы
    start_idx = current_page * tests_per_page
    end_idx = min(start_idx + tests_per_page, len(employee.test_results))
    
    for test in employee.test_results[start_idx:end_idx]:
        keyboard.add(types.InlineKeyboardButton(
            f"{test.date} - {test.type}",
            callback_data=CLTestsCallbackData(
                action="view_test",
                test_id=test._id,
                page=current_page
            ).pack()
        ))
    
    # Добавляем навигационные кнопки, если есть больше одной страницы
    nav_buttons = []
    if total_pages > 1:
        if current_page > 0:
            nav_buttons.append(types.InlineKeyboardButton(
                "⬅️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=current_page - 1
                ).pack()
            ))
        if current_page < total_pages - 1:
            nav_buttons.append(types.InlineKeyboardButton(
                "➡️",
                callback_data=CLTestsCallbackData(
                    action="change_page",
                    test_id="",
                    page=current_page + 1
                ).pack()
            ))
        if nav_buttons:
            keyboard.row(*nav_buttons)
    
    # Добавляем кнопку "Назад"
    keyboard.add(types.InlineKeyboardButton(
        "Назад",
        callback_data=employee.id
    ))
    
    await callback.message.edit_text(
        f'📊 Срезы знаний сотрудника {employee.name}:\n'
        f'Всего тестов: {len(employee.test_results)}\n'
        f'Страница {current_page + 1} из {total_pages}',
        reply_markup=keyboard
    )


def reg_cl_tests_handlers(dp: Dispatcher):
    # Регистрируем обработчик для просмотра тестов и навигации
    dp.register_callback_query_handler(
        emp_cl_tests,
        lambda c: c.data and (not c.data.startswith(CLTestsCallbackData.prefix) or 
                            CLTestsCallbackData.unpack(c.data).action == "change_page"),
        state=EmployeesSG.CLTests.Menu.state
    )
    
    dp.register_callback_query_handler(
        view_test_details,
        lambda c: c.data and CLTestsCallbackData.unpack(c.data).action == "view_test",
        state=EmployeesSG.CLTests.Menu.state
    )

    # Регистрируем обработчики для добавления теста
    dp.register_callback_query_handler(
        add_test_start,
        lambda c: c.data and CLTestsCallbackData.unpack(c.data).action == "add_test",
        state=EmployeesSG.CLTests.Menu.state
    )
    
    # Регистрируем обработчик для возврата к списку тестов
    dp.register_callback_query_handler(
        back_to_tests,
        lambda c: c.data and CLTestsCallbackData.unpack(c.data).action == "back_to_tests",
        state=EmployeesSG.CLTests.Details.state
    )
    
    dp.register_message_handler(
        add_test_date,
        state=EmployeesSG.CLTests.Add.Date.state
    )
    
    dp.register_message_handler(
        add_test_type,
        state=EmployeesSG.CLTests.Add.Type.state
    )
    
    dp.register_message_handler(
        add_test_time,
        state=EmployeesSG.CLTests.Add.Time.state
    )
    
    dp.register_message_handler(
        add_test_score,
        state=EmployeesSG.CLTests.Add.Score.state
    )
    
    dp.register_message_handler(
        add_test_rank,
        state=EmployeesSG.CLTests.Add.Rank.state
    )
    
    # Регистрируем обработчик для отмены добавления теста
    dp.register_callback_query_handler(
        cancel_add_test,
        lambda c: c.data and CLTestsCallbackData.unpack(c.data).action == "cancel_add",
        state=EmployeesSG.CLTests.Add.Date.state
    )
    
    