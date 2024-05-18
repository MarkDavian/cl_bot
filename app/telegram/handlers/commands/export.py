import pandas as pd
from aiogram import types, Dispatcher

from app.core.funcs.get_employees import func_get_employees


async def cmd_export(message: types.Message):
    employees = func_get_employees()
    emps = [employee.__dict__() for employee in employees]

    df = pd.DataFrame.from_dict(emps)
    df.to_excel('files/Сотрудники.xlsx')

    await message.reply_document(
        document=open("files/Сотрудники.xlsx", "rb"),
        caption="Таблица сотрудников"
    )


def reg_export_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_export, commands="export", state='*')