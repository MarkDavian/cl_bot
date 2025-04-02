from aiogram import types, Dispatcher
from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.commands.menu.subjects.query.table_master import TableMaster
from app.telegram.handlers.states import MenuSG

async def menu_callback_query_lmk_dates(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("Создать", callback_data=MenuCallbackData(action="create_lmk_dates_query").hash()),
        types.InlineKeyboardButton("Назад", callback_data=MenuCallbackData(action="make_query").hash())
    ]
    
    keyboard.add(*buttons)
    
    await callback.message.edit_text(
        "Этот запрос сделает таблицу сотрудников у которых есть лмк и дата его получения",
        reply_markup=keyboard
    )

async def create_lmk_dates_query(callback: types.CallbackQuery):
    employees = func_get_employees()
    
    # Сотрудники с ЛМК
    employees_with_lmk = [emp for emp in employees if emp.lmk and emp.lmk != "Не указано"]
    if employees_with_lmk:
        data = [["ФИО", "Дата получения ЛМК"]]
        for emp in employees_with_lmk:
            data.append([
                f"{emp.name}",
                emp.lmk
            ])
            
        table_master = TableMaster(data)
        xlsx_path, img_path = table_master.create_files()
        
        await callback.message.reply_document(
            open(xlsx_path, "rb"),
            caption="Сотрудники с ЛМК"
        )
        await callback.message.reply_photo(
            open(img_path, "rb")
        )
    
    # Сотрудники без ЛМК
    employees_without_lmk = [emp for emp in employees if not emp.lmk or emp.lmk == "Не указано"]
    if employees_without_lmk:
        data = [["ФИО"]]
        for emp in employees_without_lmk:
            data.append([f"{emp.name}"])
            
        table_master = TableMaster(data)
        xlsx_path, img_path = table_master.create_files()
        
        await callback.message.reply_document(
            open(xlsx_path, "rb"),
            caption="Сотрудники без ЛМК"
        )
        await callback.message.reply_photo(
            open(img_path, "rb")
        )
        
    table_master.delete_files()

def reg_lmk_dates_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_query_lmk_dates,
        lambda c: c.data == MenuCallbackData(action="query_lmk_dates").hash(),
        state=MenuSG.Menu.state
    )
    dp.register_callback_query_handler(
        create_lmk_dates_query,
        lambda c: c.data == MenuCallbackData(action="create_lmk_dates_query").hash(),
        state=MenuSG.Menu.state
    )
