from aiogram import types, Dispatcher
from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.commands.menu.subjects.query.table_master import TableMaster
from app.telegram.handlers.states import MenuSG


async def menu_callback_query_exp_dates(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("Создать", callback_data=MenuCallbackData(action="create_exp_query").hash()),
        types.InlineKeyboardButton("Назад", callback_data=MenuCallbackData(action="make_query").hash())
    ]
    
    keyboard.add(*buttons)
    
    await callback.message.edit_text(
        "Этот запрос сделает таблицу сотрудников со стажем работы",
        reply_markup=keyboard
    )

async def create_exp_dates_query(callback: types.CallbackQuery):
    employees = func_get_employees()
    
    data = [["ФИО", "Возраст", "Дата начала работы", "Стаж"]]
    for emp in employees:
        data.append([
            f"{emp.name}",
            emp.get_years_old(),
            emp.workstarted,
            emp.get_experience()
        ])
            
    table_master = TableMaster(data)
    xlsx_path, img_path = table_master.create_files()
    
    await callback.message.reply_document(
        open(xlsx_path, "rb"),
        caption="Сотрудники"
    )
    await callback.message.reply_photo(
        open(img_path, "rb")
    )
    
    table_master.delete_files()


def reg_exp_dates_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_query_exp_dates,
        lambda c: c.data == MenuCallbackData(action="query_work_experience").hash(),
        state=MenuSG.Menu.state
    )
    dp.register_callback_query_handler(
        create_exp_dates_query,
        lambda c: c.data == MenuCallbackData(action="create_exp_query").hash(),
        state=MenuSG.Menu.state
    )
