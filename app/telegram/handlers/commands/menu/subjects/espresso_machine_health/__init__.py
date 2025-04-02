from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from app.telegram.handlers.commands.menu.common import MenuCallbackData
from app.telegram.handlers.states import MenuSG, EspressoSG
from app.core.funcs.espresso_machine import func_get_espresso_gasket_replacement_date, func_get_espresso_health_bar

from .common import EspressoCallbackData
from .espresso_machines import reg_espresso_handlers


async def menu_callback_espresso_health_main(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EspressoSG.Menu.state)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        types.InlineKeyboardButton("⬅️ Назад", callback_data=MenuCallbackData(action="main_menu").hash()),
        types.InlineKeyboardButton("☕️ Кофемашины", callback_data=EspressoCallbackData(action="show_machines").pack())
    ]

    keyboard.add(*buttons)

    await callback.message.edit_text(
        "❤️‍🩹Здоровье кофемашин:\n"
        f"{func_get_espresso_health_bar()}\n"
        f"🔴 Требуется замена резинок-уплотнителей в следующих кофемашинах:\n"
        f"{func_get_espresso_gasket_replacement_date()}\n",
        reply_markup=keyboard
    )


def reg_espresso_health_main_callback(dp: Dispatcher):
    dp.register_callback_query_handler(
        menu_callback_espresso_health_main, 
        lambda c: c.data == MenuCallbackData(action="espresso_health").hash(), 
        state='*'
    )
    reg_espresso_handlers(dp)



