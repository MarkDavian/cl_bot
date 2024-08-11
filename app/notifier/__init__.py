import asyncio

import time

from aiogram import Bot

from config import SETTINGS

from app.notifier.check_birthday import check_birthday
from app.notifier.check_lmk import check_lmk


async def _start_notifier():
    bot = Bot(SETTINGS.BOT_TOKEN, parse_mode='html')

    while True:
        employees_birthday = check_birthday()
        employees_lmk = check_lmk()
        if len(employees_birthday) != 0:
            for employee in employees_birthday:
                await bot.send_message(
                    chat_id=SETTINGS.CHAT,
                    text=(
                        "<b>СКОРО ДЕНЬ РОЖДЕНИЯ</b>\n"
                        f"<b>Сотрудник:</b> {employee.name}\n"
                        f"<b>Дата рождения:</b> {employee.birthday}\n"
                        f"<b>Полных лет:</b> {employee.get_years_old()}\n\n"
                        f"<b>ДР через (дней):</b> {employee.get_days_to()}"
                    )
                )
        if len(employees_lmk) != 0:
            for employee in employees_lmk:
                await bot.send_message(
                    chat_id=SETTINGS.CHAT,
                    text=(
                            "<b>ОБРАТИ ВНИМАНИЕ НА МЕДКНИЖКУ</b>\n"
                            f"Сотрудник: {employee.name}\n"
                            f"Полных лет: {employee.get_years_old()}\n\n"
                            f"ЛМК от: {employee.lmk}"
                    )
                )
        time.sleep(SETTINGS.INTERVAL_24*2)


def start_notifier():
    asyncio.run(_start_notifier())