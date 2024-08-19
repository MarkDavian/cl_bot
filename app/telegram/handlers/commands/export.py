import pandas as pd

from aiogram import Bot
from aiogram import types, Dispatcher

from config import SETTINGS
from app.core.funcs.get_employees import func_get_employees


async def cmd_export(message: types.Message):
    employees = func_get_employees()
    emps = [employee.__dict__() for employee in employees]

    df = pd.DataFrame.from_dict(emps)
    df.to_excel('files/Сотрудники.xlsx')

    bot = Bot(SETTINGS.BOT_TOKEN, parse_mode='html')


    await bot.send_document(
            chat_id=-1002156206771,
            document=open("files/Сотрудники.xlsx", "rb"),
            caption="Таблица сотрудников"
        )
    await bot.send_document(
            chat_id=-1002156206771,
            document=open("storage/storage.json", "rb"),
            caption="Storage сотрудников"
        )


def reg_export_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_export, commands="export", state='*')