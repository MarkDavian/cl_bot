import pandas as pd

from aiogram import types, Dispatcher

from app.core.funcs.get_employees import func_get_employees
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.states import MenuSG


async def menu_callback_export(callback: types.CallbackQuery):
    bot = callback.message.bot
    employees = func_get_employees()
    emps = [employee.__dict__() for employee in employees]

    df = pd.DataFrame.from_dict(emps)
    df.to_excel('files/Сотрудники.xlsx')

    await bot.send_document(
            chat_id=callback.message.chat.id,
            document=open("files/Сотрудники.xlsx", "rb"),
            caption="Таблица сотрудников"
        )
    await bot.send_document(
            chat_id=callback.message.chat.id,
            document=open("storage/storage.json", "rb"),
            caption="Storage сотрудников"
        )


def reg_export_callback(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_export, 
        lambda c: c.data == MenuCallbackData(action="export_xlsx").hash(), 
        state=MenuSG.Menu.state
    )