import pandas as pd

from aiogram import types, Dispatcher

from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.states import MenuSG

from app.telegram.handlers.commands.menu.subjects.query.queries.lmk_start_dates import reg_lmk_dates_handlers
from app.telegram.handlers.commands.menu.subjects.query.queries.birthdays import reg_dr_dates_handlers
from app.telegram.handlers.commands.menu.subjects.query.queries.exp_emp import reg_exp_dates_handlers
from app.telegram.handlers.commands.menu.subjects.query.queries.expired_lmk import reg_lmk_exp_dates_handlers
from app.telegram.handlers.commands.menu.subjects.query.queries.birthdays_in_month import reg_birthdays_month_handlers
from app.telegram.handlers.commands.menu.subjects.query.queries.certificates import reg_certificates_handlers

async def menu_callback_query_main(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("ЛМК. Даты получения", callback_data=MenuCallbackData(action="query_lmk_dates").hash()),
        types.InlineKeyboardButton("Просроченные ЛМК", callback_data=MenuCallbackData(action="query_expired_lmks").hash()),
        types.InlineKeyboardButton("Дни рождения сотрудников", callback_data=MenuCallbackData(action="query_dr_dates").hash()),
        types.InlineKeyboardButton("Дни рождения в этом месяце", callback_data=MenuCallbackData(action="query_birthdays_this_month").hash()),
        types.InlineKeyboardButton("Стаж работы", callback_data=MenuCallbackData(action="query_work_experience").hash()),
        types.InlineKeyboardButton("Сертификаты сотрудников", callback_data=MenuCallbackData(action="query_certificates").hash())
    ]

    keyboard.add(*buttons)

    await callback.message.edit_text(
        "Выберите тип запроса:",
        reply_markup=keyboard
    )


def reg_query_main_callback(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_query_main, 
        lambda c: c.data == MenuCallbackData(action="make_query").hash(), 
        state=MenuSG.Menu.state
    )
    reg_lmk_dates_handlers(dp)
    reg_dr_dates_handlers(dp)
    reg_exp_dates_handlers(dp)
    reg_lmk_exp_dates_handlers(dp)
    reg_birthdays_month_handlers(dp)
    reg_certificates_handlers(dp)