from aiogram import types, Dispatcher


async def cmd_start(message: types.Message):
    await message.reply_document(
        open('files/Презентация бота.pdf', 'rb'),
        "Привет! Ознакомься с инструкцией)"
    )


def reg_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")