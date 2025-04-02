import os
from aiogram import types, Dispatcher
from aiogram import Bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext


from app.telegram.handlers.states import EmployeesSG
from app.telegram.handlers.commands.emps_ext.menu_subjects.emps_sub_CLTests import emp_cl_tests, emp_cl_tests, reg_cl_tests_handlers
from app.core.funcs.get_employees import func_get_employees, func_get_by_id
from app.core.funcs.correct_date import date_incorrect
from app.core.funcs.add_employee import func_add_employee
from app.core.funcs.del_employee import func_del_emp
from app.core.funcs.file.path import Certificates
from app.core.funcs.file.encoder import uniq_name
from app.core.types.types import EmployeeBuilder
from .common import EmpCallbackData, CLTestsCallbackData


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

    if callback.data.startswith('back'):
        emp_id = callback.data[5:]
    else:
        emp_id = callback.data
    employee = func_get_by_id(emp_id)

    await state.set_data({'employee': employee.__dict__()})

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        types.InlineKeyboardButton('❌Удалить', callback_data='Delete'),
        types.InlineKeyboardButton('📋Изменить', callback_data='Change')
    )
    keyboard.add(types.InlineKeyboardButton('📃Сертификаты', callback_data='Certificates'))
    keyboard.add(types.InlineKeyboardButton('🥇Срезы знаний', callback_data='CLTests'))
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data='employees'))

    try:
        await callback.message.edit_text(
            f'<b>ФИО сотрудника:</b> {employee.name}\n'
            f'<b>Дата рождения:</b> {employee.birthday}\n'
            f'<b>Полных лет:</b> {employee.get_years_old()}\n'
            f'<b>ДР через (дней):</b> {employee.get_days_to_birth()}\n'
            f'<b>Начало работы:</b> {employee.workstarted}\n'
            f'<b>Стаж работы:</b> {employee.get_experience()}\n'
            f'<b>ЛМК от:</b> {employee.lmk}\n'
            f'<b>Базовый сертификат от:</b> {employee.cert_base}\n'
            f'<b>Профи сертификат от:</b> {employee.cert_profi}\n\n'
            f'<b>ID:</b> {employee.id}\n'
            f'<b>Дата регистрации:</b> {employee.registration}\n',
            reply_markup=keyboard
        )
    except Exception as e:
        chat_id = callback.message.chat.id
        await callback.message.delete()
        await callback.message.bot.send_message(
            chat_id,
            f'<b>ФИО сотрудника:</b> {employee.name}\n'
            f'<b>Дата рождения:</b> {employee.birthday}\n'
            f'<b>Полных лет:</b> {employee.get_years_old()}\n'
            f'<b>ДР через (дней):</b> {employee.get_days_to_birth()}\n'
            f'<b>Начало работы:</b> {employee.workstarted}\n'
            f'<b>Стаж работы:</b> {employee.get_experience()}\n'
            f'<b>ЛМК от:</b> {employee.lmk}\n'
            f'<b>Базовый сертификат от:</b> {employee.cert_base}\n'
            f'<b>Профи сертификат от:</b> {employee.cert_profi}\n\n'
            f'<b>ID:</b> {employee.id}\n'
            f'<b>Дата регистрации:</b> {employee.registration}\n',
            reply_markup=keyboard
        )


async def emp_certificates(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Certificates_menu.state)

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    certificates = []
    certificates_exist = False
    if os.path.exists(Certificates.path+employee.id) and any(f.startswith('CRT') for f in os.listdir(Certificates.path+employee.id)):
        certificates_exist = True

    if certificates_exist:
        for filename in os.listdir(Certificates.path+employee.id):
            if os.path.isfile(os.path.join(Certificates.path+employee.id, filename)):
                if filename.startswith('CRT'):
                    certificates.append(filename)


    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))
    if certificates_exist: 
        keyboard.add(types.InlineKeyboardButton('Удалить все сертификаты', callback_data='DeleteAllCerts'))
        keyboard.add(
            *[
                types.InlineKeyboardButton(
                    text=filename, 
                    callback_data=filename
                ) 
                for filename in certificates
            ]
        )


    await callback.message.edit_text(
        f'<b>ФИО сотрудника:</b> {employee.name}\n'
        f'<b>Базовый сертификат от:</b> {employee.cert_base}\n'
        f'<b>До:</b> {employee.get_cert_expire_date("base")}\n'
        f'<b>Профи сертификат от:</b> {employee.cert_profi}\n'
        f'<b>До:</b> {employee.get_cert_expire_date("profi")}\n\n',
        reply_markup=keyboard
    )


async def delete_all_certificates(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Certificates_delete.state)

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data="Certificates"))
    keyboard.add(types.InlineKeyboardButton('УДАЛИТЬ', callback_data=f'DeleteAllCertsOk'))

    await callback.message.edit_text(
        f'Вы уверены, что хотите удалить все сертификаты сотрудника {employee.name}?',
        reply_markup=keyboard
    )   


async def delete_all_certificates_ok(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()   

    for filename in os.listdir(Certificates.path+employee.id):
        if os.path.isfile(os.path.join(Certificates.path+employee.id, filename)):
            if filename.startswith('CRT'):
                os.remove(os.path.join(Certificates.path+employee.id, filename))            
                
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад к сотруднику', callback_data=employee.id))

    await callback.message.edit_text(
        f'Все сертификаты сотрудника {employee.name} удалены',
        reply_markup=keyboard
    )

    await state.set_state(EmployeesSG.Certificates_menu.state)


async def certificate_view(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    # filename = callback.data
    # path_to_certificate = Certificates.path+filename
    filename = callback.data
    path_to_certificate = Certificates.path+employee.id+'/'+filename

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))
    keyboard.add(types.InlineKeyboardButton(
        'Скачать ФАЙЛ', 
        callback_data=f'Crtdwnld_{filename}'
    ))
    
    keyboard.add(types.InlineKeyboardButton(
        '❌УДАЛИТЬ',
        callback_data=f'Crtdlt_{filename}'
    ))


    bot = callback.message.bot
    with open(path_to_certificate, 'rb') as file:
        photo = types.InputMediaPhoto(file, caption=f"Сертификат бариста {employee.name}")
        await bot.edit_message_media(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id,
            media=photo,
            reply_markup=keyboard
        )


async def certificate_download(callback: types.CallbackQuery, state: FSMContext):
    bot: Bot = callback.message.bot

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    filename = callback.data[9:]
    path_to_certificate = Certificates.path+employee.id+'/'+filename
    
    with open(path_to_certificate, 'rb') as file:
        document = types.InputFile(file)
        await bot.send_document(callback.message.chat.id, document)


async def certificate_delete(callback: types.CallbackQuery, state: FSMContext):
    bot: Bot = callback.message.bot
    chat_id = callback.message.chat.id

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    filename = callback.data[7:]
    path_to_certificate = Certificates.path+employee.id+'/'+filename

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад к сертификатам', callback_data=employee.id))

    msg = '<b>Ошибка при удалении файла</b>\n'
    try:
        os.remove(path_to_certificate)
        msg ='<b>Сертификат удалён</b>\n'
    except FileNotFoundError:
        msg = '<b>Файл не найден</b>\n'
    except PermissionError:
        await callback.message.edit_text(
            f'<b>Нет прав для удаления файла</b>\n',
            reply_markup=keyboard
        )
    except OSError as e:
        print(f'Ошибка при удалении файла {path_to_certificate}', e)

    await callback.message.delete()
    await callback.message.bot.send_message(
        chat_id,
        msg,
        reply_markup=keyboard
    )


async def delete_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Delete.state)

    data = await state.get_data()
    employee = data.get('employee')

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee['id']))
    keyboard.add(types.InlineKeyboardButton('❌УДАЛИТЬ', callback_data='Delete'))

    await callback.message.edit_text(
        f'ФИО сотрудника: {employee["name"]}\n'
        f'<b>ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ УДАЛИТЬ СОТРУДНИКА?</b>',
        reply_markup=keyboard
    )


async def sucker(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    employee = data.get('employee')

    emp = func_del_emp(employee['id'])

    await callback.message.edit_text(
        f'ФИО сотрудника: {emp["name"]}\n'
        f'<b>СОТРУДНИК УДАЛЕН</b>'
    )

    await state.finish()


async def change_emp(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change.state)
    
    data = await state.get_data()
    employee = data.get('employee')

    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('ФИО сотрудника', callback_data="name"))
    keyboard.add(types.InlineKeyboardButton('Дата рождения', callback_data="birthday"))
    keyboard.add(types.InlineKeyboardButton('Начало работы', callback_data="workstarted"))
    keyboard.add(types.InlineKeyboardButton('ЛМК', callback_data="lmk"))
    keyboard.add(types.InlineKeyboardButton('Базовый сертификат', callback_data="cert_base"))
    keyboard.add(types.InlineKeyboardButton('Профи сертификат', callback_data="cert_profi"))
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'<b>ФИО сотрудника:</b> {employee.name}\n'
        f'<b>Дата рождения:</b> {employee.birthday}\n'
        f'<b>Полных лет:</b> {employee.get_years_old()}\n'
        f'<b>ДР через (дней):</b> {employee.get_days_to_birth()}\n'
        f'<b>Начало работы:</b> {employee.workstarted}\n'
        f'<b>Стаж работы:</b> {employee.get_experience()}\n'
        f'<b>ЛМК от:</b> {employee.lmk}\n'
        f'<b>Базовый сертификат от:</b> {employee.cert_base}\n'
        f'<b>Профи сертификат от:</b> {employee.cert_profi}\n\n'
        f'<b>ID:</b> {employee.id}\n'
        f'<b>Дата регистрации:</b> {employee.registration}\n\n'
        f'<b>ЧТО ХОТИТЕ ИЗМЕНИТЬ?</b>',
        reply_markup=keyboard
    )


async def change_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_name.state)

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши ФИО сотрудника',
        reply_markup=keyboard
    )


async def change_name_end(message: types.Message, state: FSMContext):
    name = message.text

    data = await state.get_data()
    employee = data.get('employee')
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

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату рождения сотрудника',
        reply_markup=keyboard
    )


async def change_birthday_end(message: types.Message, state: FSMContext):
    birthday = message.text

    incorrect = date_incorrect(birthday)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
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

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату начала работы сотрудника',
        reply_markup=keyboard
    )


async def change_workstarted_end(message: types.Message, state: FSMContext):
    workstarted = message.text

    incorrect = date_incorrect(workstarted)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
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

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Напиши дату получения ЛМК сотрудника',
        reply_markup=keyboard
    )


async def change_lmk_end(message: types.Message, state: FSMContext):
    lmk = message.text

    incorrect = date_incorrect(lmk)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
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


async def change_cert_base(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_cert_base.state)

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Загрузи новый сертификат <b>Базового Курса</b>.\n'
        f'Загрузи его как PDF или как Обычное ФОТО в виде файла (.jpg, .heic, .png)',
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def another_one_cert_base(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Отмена', callback_data='end_cert_base'))

    await callback.message.edit_text(
        f'Загрузи сертификат <b>Базового Курса</b>.\n'
        f'Загрузи его как PDF или как Обычное ФОТО в виде файла (.jpg, .heic, .png)',
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def change_cert_base_download(message: types.Message, state: FSMContext):
    from app.core.funcs.file.path import Certificates
    from app.core.funcs.file.encoder import uniq_name

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    extension = message.document.file_name.split('.')[-1]
    path = Certificates.path+employee.id    
    if not os.path.exists(path):
        os.makedirs(path)
    destination = path+'/'+uniq_name()+'.'+extension

    await message.document.download(destination=destination)

    
    employee.cert_base_path.append(destination)
    await state.set_data({'employee': employee.__dict__()})

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Нет. Это всё', callback_data='end_cert_base'))
    keyboard.add(types.InlineKeyboardButton('Добавить', callback_data='download_another_one_base_cert'))

    await message.reply(
        f'Файл загружен.\n'
        f'<b>Добавить еще файл?</b>',
        reply_markup=keyboard
    )


async def end_cert_base(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Сертификаты загружены!\n'
        'Теперь напиши дату получения сертификатов сотрудником:'
    )


async def date_end_cert_base(message: types.Message, state: FSMContext):
    cert_date = message.text

    incorrect = date_incorrect(cert_date)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    employee.cert_base = cert_date

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новая дата прохождения <b>Базового Курса</b> сотрудника:\n'
        f'<b>{cert_date}</b>',
        reply_markup=keyboard
    )


async def change_cert_profi(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Change_cert_profi.state)

    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('🔙Назад', callback_data=employee.id))

    await callback.message.edit_text(
        f'Загрузи новый сертификат <b>Профи Курса</b>.\n'
        f'Загрузи его как PDF или как Обычное ФОТО (.jpg, .heic, .png)',
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def another_one_cert_profi(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Отмена', callback_data='end_cert_profi'))

    await callback.message.edit_text(
        f'Загрузи сертификат <b>Профи Курса</b>.\n'
        f'Загрузи его как PDF или как Обычное ФОТО (.jpg, .heic, .png)',
        reply_markup=keyboard,
        parse_mode='HTML'
    )


async def change_cert_profi_download(message: types.Message, state: FSMContext):
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()

    extension = message.document.file_name.split('.')[-1]
    destination = Certificates.path+employee.id+'/'+uniq_name()+'.'+extension
    await message.document.download(destination=destination)
    
    employee.cert_profi_path.append(destination)
    await state.set_data({'employee': employee.__dict__()})

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Нет. Это всё', callback_data='end_cert_profi'))
    keyboard.add(types.InlineKeyboardButton('Добавить', callback_data='download_another_one_profi_cert'))

    await message.reply(
        f'Файл загружен.\n'
        f'<b>Добавить еще файл?</b>',
        reply_markup=keyboard
    )


async def end_cert_profi(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Сертификаты загружены!\n'
        'Теперь напиши дату получения сертификатов сотрудником:'
    )


async def date_end_cert_profi(message: types.Message, state: FSMContext):
    cert_date = message.text

    incorrect = date_incorrect(cert_date)
    if incorrect:
        await message.reply(
            f"{incorrect}"
            "❗️Обрати внимание: дата должна быть в формате <b>ДД.ММ.ГГГГ</b>"
        )
        return
    
    data = await state.get_data()
    employee = data.get('employee')
    employee = EmployeeBuilder(**employee).get_employee()
    employee.cert_profi = cert_date

    func_del_emp(employee.id)
    func_add_employee(**employee.__dict__())

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('👨🏻К сотруднику', callback_data=employee.id))

    await message.reply(
        f'Новая дата прохождения <b>Профи Курса</b> сотрудника:\n'
        f'<b>{cert_date}</b>',
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
    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data.startswith('back'), state=EmployeesSG.CLTests.Menu)

    dp.register_callback_query_handler(certificate_download, lambda callback: callback.data.startswith('Crtdwnld'), state=EmployeesSG.Certificates_menu)
    dp.register_callback_query_handler(certificate_delete, lambda callback: callback.data.startswith('Crtdlt'), state=EmployeesSG.Certificates_menu)
    dp.register_callback_query_handler(certificate_view, lambda callback: "CRT" in callback.data, state=EmployeesSG.Certificates_menu)

    dp.register_callback_query_handler(delete_all_certificates, lambda callback: callback.data == 'DeleteAllCerts', state=EmployeesSG.Certificates_menu)

    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Certificates_menu)


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

    dp.register_callback_query_handler(change_cert_base, lambda callback: callback.data == 'cert_base', state=EmployeesSG.Change)
    dp.register_callback_query_handler(another_one_cert_base, lambda callback: callback.data == 'download_another_one_base_cert', state=EmployeesSG.Change_cert_base)
    dp.register_message_handler(change_cert_base_download, state=EmployeesSG.Change_cert_base, content_types='document')
    dp.register_callback_query_handler(end_cert_base, lambda callback: callback.data == 'end_cert_base', state=EmployeesSG.Change_cert_base)
    dp.register_message_handler(date_end_cert_base, state=EmployeesSG.Change_cert_base)

    dp.register_callback_query_handler(change_cert_profi, lambda callback: callback.data == 'cert_profi', state=EmployeesSG.Change)
    dp.register_callback_query_handler(another_one_cert_profi, lambda callback: callback.data == 'download_another_one_profi_cert', state=EmployeesSG.Change_cert_profi)
    dp.register_message_handler(change_cert_profi_download, state=EmployeesSG.Change_cert_profi, content_types='document')
    dp.register_callback_query_handler(end_cert_profi, lambda callback: callback.data == 'end_cert_profi', state=EmployeesSG.Change_cert_profi)
    dp.register_message_handler(date_end_cert_profi, state=EmployeesSG.Change_cert_profi)

    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_cert_base)
    dp.register_callback_query_handler(choose_emp, lambda callback: callback.data, state=EmployeesSG.Change_cert_profi)

    dp.register_callback_query_handler(emp_certificates, lambda callback: callback.data == 'Certificates', state=EmployeesSG.Employee)
    dp.register_callback_query_handler(emp_cl_tests, lambda callback: callback.data == 'CLTests', state=EmployeesSG.Employee)
    
    dp.register_callback_query_handler(delete_all_certificates_ok, lambda callback: callback.data == 'DeleteAllCertsOk', state=EmployeesSG.Certificates_delete)

    # dp.register_callback_query_handler(change_cert_profi, lambda callback: callback.data == 'cert_profi', state=EmployeesSG.Change)
    # dp.register_message_handler(change_cert_profi_end, state=EmployeesSG.Change_cert_profi)

    dp.register_callback_query_handler(choose_emp, state=EmployeesSG.Change)

    reg_cl_tests_handlers(dp)