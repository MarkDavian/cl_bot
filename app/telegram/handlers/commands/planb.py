import os
import pandas as pd
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import PlanB
from app.core.funcs.get_employees import func_get_employees


async def cmd_planb(message: types.Message, state: FSMContext):
    await state.finish()

    employees = func_get_employees()
    emps = [employee.__dict__() for employee in employees]

    df = pd.DataFrame.from_dict(emps)
    df.to_excel('files/Сотрудники.xlsx')

    await message.reply(
        "Жду файл .json"
    )
    await state.set_state(PlanB.wait.state)


async def get_file(message: types.Message, state: FSMContext):
    if message.content_type != "document":
        await message.reply("Нужен файл типа .json")
        return 

    ext = message.document.file_name.split('.')[-1]
    filename = f"new_base.{ext}"

    with open(f'files/{filename}', 'wb') as file:
        await message.document.download(file)

    r = await new_base_create(filename)
    if r is None:
        await message.reply(
            'База сохранена'
        )
        await state.finish()
    else:
        await message.reply("Что-то пошло не так, попробуй еще раз")
        return


async def new_base_create(filename: str):
    try:
        os.remove('storage/storage.json')
        os.replace(f"files/{filename}", f"storage/{filename}")
        os.rename(f"storage/{filename}", f"storage/storage.json")
        return None
    except Exception as e:
        return e


def reg_planb_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_planb, commands="planb", state='*')
    dp.register_message_handler(get_file, state=PlanB.wait, content_types='document')