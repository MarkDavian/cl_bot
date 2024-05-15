from aiogram import types, Dispatcher


async def cmd_start(message: types.Message):
    await message.reply(
            "Привет! Скинь мне таблицу сотрудников, чтобы начать. Или добавь сотрудников вручную командой /add"
    )


def reg_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")