import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def view_service_details(message: types.Message, state: FSMContext):
    """
    View details of a Telegram user by ID
    Usage: /whois <user_id>
    """
    # Extract user_id from command
    command_pattern = r"^\/whois(\d+)$"
    match = re.match(command_pattern, message.text)
    
    if not match:
        await message.reply("Используйте команду в формате: /whois<user_id>")
        return
    
    user_id = match.group(1)
    
    try:
        # Try to get user info from Telegram
        user_info = await message.bot.get_chat(user_id)
        username = user_info.username
        full_name = user_info.full_name
        
        response = f"📋 Информация о пользователе:\n\n"
        response += f"🆔 ID: {user_id}\n"
        response += f"👤 Имя: {full_name}\n"
        
        if username:
            response += f"🔗 Ссылка: @{username}\n"
            response += f"🌐 Профиль: https://t.me/{username}"
        else:
            response += "❌ У пользователя нет username"
            
        await message.reply(response)
    except Exception as e:
        await message.reply(f"❌ Не удалось найти пользователя с ID {user_id}\n\nОшибка: {str(e)}")


def register_whois_handler(dp: Dispatcher):
    """Register handler for the /whois command"""
    dp.register_message_handler(view_service_details, regexp=r"^\/whois(\d+)$", state="*")
