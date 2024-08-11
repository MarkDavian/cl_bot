import asyncio

import pandas as pd
from aiogram import Bot

from config import SETTINGS

from app.core.funcs.get_employees import func_get_employees


async def backup():
    bot = Bot(SETTINGS.BOT_TOKEN, parse_mode='html')

    while True:
        employees = func_get_employees()
        emps = [employee.__dict__() for employee in employees]

        df = pd.DataFrame.from_dict(emps)
        df.to_excel('files/Сотрудники.xlsx')

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
        await asyncio.sleep(SETTINGS.INTERVAL_24)

def start_backup():
    asyncio.run(backup())