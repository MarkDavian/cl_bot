from aiogram import Dispatcher
from aiogram.types import Message
from app.notifier.check_lmk import check_lmk
from datetime import datetime, timedelta


async def lmk_list(message: Message):
    """
    Sends a list of employees whose LMK (Medical Book) is expiring, and when it will expire.
    """
    employees_with_expiring_lmk = check_lmk()

    if not employees_with_expiring_lmk:
        await message.reply(
            text="<b>На данный момент нет сотрудников с истекающим ЛМК.</b>"
        )
        return

    response_text = "<b>Сотрудники с истекающим ЛМК:</b>\n\n"
    for employee in employees_with_expiring_lmk:
        days_until_expiration = employee.get_days_lmk()
        if days_until_expiration == "Неизвестно":
            expiration_date_text = "Неизвестно"
        else:
            expiration_date = datetime.now() + timedelta(days=days_until_expiration)
            expiration_date_text = expiration_date.strftime("%d.%m.%Y")
        response_text += (
            f"<b>Сотрудник:</b> {employee.name}\n"
            f"<b>Дата ЛМК:</b> {employee.lmk}\n"
            f"<b>Истекает через (дней):</b> {days_until_expiration}\n"
            f"<b>Дата истечения:</b> {expiration_date_text}\n\n"
        )

    await message.reply(
        text=response_text,
        parse_mode='html'
    )


def reg_lmk_list(dp: Dispatcher):
    dp.register_message_handler(lmk_list, commands="lmk_list", state='*')

