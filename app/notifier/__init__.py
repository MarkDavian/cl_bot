import asyncio

import time

from aiogram import Bot

from config import SETTINGS

from app.notifier.check_birthday import check_birthday
from app.notifier.check_lmk import check_lmk


async def _start_notifier():
    bot = Bot(SETTINGS.BOT_TOKEN, parse_mode='html')

    while True:
        employees = check_birthday()
        if len(employees) != 0:
            for employee in employees:
                await bot.send_message(
                    chat_id=SETTINGS.CHAT,
                    text=(
                        f"<b>Сотрудник:</b> {employee.name}\n"
                        f"<b>Дата рождения:</b> {employee.birthday}\n"
                        f"<b>Полных лет:</b> {employee.get_years_old()}\n\n"
                        f"<b>ДР через (дней):</b> {employee.get_days_to()}"
                    )
                )
        # if employee := check_lmk():
        #     await bot.send_message(
        #         chat_id=SETTINGS.CHAT,
        #         text=(
        #                 f"Сотрудник: {employee.name}"
        #                 f"Дата рождения: {employee.birthday}"
        #                 f"Полных лет: {employee.get_years_old()}"
        #                 f"ЛМК от: {employee.lmk}"
        #         )
        #     )
        # time.sleep(SETTINGS.INTERVAL)
        await asyncio.sleep(5)


def start_notifier():
    asyncio.run(_start_notifier())