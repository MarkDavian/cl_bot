from aiogram import types, Dispatcher
from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.commands.menu.subjects.query.table_master import TableMaster
from app.telegram.handlers.states import MenuSG


async def menu_callback_query_birthdays_month(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("Создать", callback_data=MenuCallbackData(action="create_birthdays_month_query").hash()),
        types.InlineKeyboardButton("Назад", callback_data=MenuCallbackData(action="make_query").hash())
    ]
    
    keyboard.add(*buttons)
    
    await callback.message.edit_text(
        "Этот запрос сделает таблицу сотрудников, у которых день рождения в ближайшие 30 дней",
        reply_markup=keyboard
    )

async def create_birthdays_month_query(callback: types.CallbackQuery):
    employees = func_get_employees()
    
    data = [["ФИО", "Дата рождения", "Дней до ДР"]]
    for emp in employees:
        try:
            days_to = emp.get_days_to_birth()
            if days_to < 31:
                data.append([
                    emp.name,
                    emp.birthday,
                    "завтра" if days_to == 0 else f"через {days_to} дней"
                ])
        except Exception:
            continue
            
    if len(data) == 1:  # Только заголовок
        await callback.message.edit_text("В ближайшие 30 дней дней рождения нет")
        return
        
    table_master = TableMaster(data)
    xlsx_path, img_path = table_master.create_files()
    
    await callback.message.reply_document(
        open(xlsx_path, "rb"),
        caption="Дни рождения в ближайшие 30 дней"
    )
    await callback.message.reply_photo(
        open(img_path, "rb")
    )

    table_master.delete_files()


def reg_birthdays_month_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_query_birthdays_month,
        lambda c: c.data == MenuCallbackData(action="query_birthdays_this_month").hash(),
        state=MenuSG.Menu.state
    )
    dp.register_callback_query_handler(
        create_birthdays_month_query,
        lambda c: c.data == MenuCallbackData(action="create_birthdays_month_query").hash(),
        state=MenuSG.Menu.state
    )
