from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import MenuSG, EspressoSG

from .common import MenuCallbackData
from .common import MenuButton

from .callback_handler import reg_callback_menu

async def _menu(message: types.Message, state: FSMContext, call: bool = False, callback: types.CallbackQuery = None):
    await state.finish()
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        MenuButton("➕ Сделать запрос", MenuCallbackData(action="make_query")),
        MenuButton("❤️‍🩹Здоровье кофемашины", MenuCallbackData(action="espresso_health")),
        MenuButton("📈 Экспорт данных", MenuCallbackData(action="export_xlsx")),
    ]

    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(
                button.text, callback_data=button.callback_data.hash()
            )
        )

    if call:    
        await callback.message.edit_text("Меню:", reply_markup=keyboard)
    else:
        await message.reply("Меню:", reply_markup=keyboard)

    await state.set_state(MenuSG.Menu.state)


async def cmd_menu(message: types.Message, state: FSMContext):
    await _menu(message, state)


async def callback_menu(callback: types.CallbackQuery, state: FSMContext):
    await _menu(callback.message, state, call=True, callback=callback)


def reg_menu_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_menu, commands='menu', state='*')
    dp.register_callback_query_handler(
        callback_menu, 
        lambda c: c.data == MenuCallbackData(action="main_menu").hash(), 
        state=EspressoSG.Menu.state
    )
    reg_callback_menu(dp)
