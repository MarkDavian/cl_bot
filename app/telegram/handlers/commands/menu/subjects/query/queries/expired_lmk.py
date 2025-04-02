from aiogram import types, Dispatcher
from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.commands.menu.subjects.query.table_master import TableMaster
from app.telegram.handlers.states import MenuSG
from datetime import datetime


async def menu_callback_query_exp_dates(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("Создать", callback_data=MenuCallbackData(action="create_lmk_exp_query").hash()),
        types.InlineKeyboardButton("Назад", callback_data=MenuCallbackData(action="make_query").hash())
    ]
    
    keyboard.add(*buttons)
    
    await callback.message.edit_text(
        "Этот запрос создаст таблицу сотрудников с истекшим сроком действия ЛМК",
        reply_markup=keyboard
    )

async def create_exp_dates_query(callback: types.CallbackQuery):
    employees = func_get_employees()
    data = [["ФИО", "Получил ЛМК", "ЛМК истекает"]]
    for emp in employees:
        if emp.lmk == "Не указано":
            continue
        try:
            lmk_date = datetime.strptime(emp.lmk, '%d.%m.%Y')
            lmk_expiry = lmk_date.replace(year=lmk_date.year + 1)
            
            if lmk_expiry < datetime.now():
                data.append([
                    f"{emp.name}",
                    emp.lmk,
                    lmk_expiry.strftime('%d.%m.%Y')
                ])
        except ValueError:
            continue
    
    if len(data) == 1:
        await callback.message.reply("Нет сотрудников с истекшим сроком действия ЛМК")
        return
            
    table_master = TableMaster(data)
    xlsx_path, img_path = table_master.create_files()
    
    await callback.message.reply_document(
        open(xlsx_path, "rb"),
        caption="Сотрудники с истекшим сроком действия ЛМК"
    )
    await callback.message.reply_photo(
        open(img_path, "rb")
    )
    
    table_master.delete_files() 

def reg_lmk_exp_dates_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_query_exp_dates,
        lambda c: c.data == MenuCallbackData(action="query_expired_lmks").hash(),
        state=MenuSG.Menu.state
    )
    dp.register_callback_query_handler(
        create_exp_dates_query,
        lambda c: c.data == MenuCallbackData(action="create_lmk_exp_query").hash(),
        state=MenuSG.Menu.state
    )
