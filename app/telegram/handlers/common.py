from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    markup = types.ReplyKeyboardRemove()
    await message.reply(
        'Действие отменено',
        reply_markup=markup
    )


def reg_cancel_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')