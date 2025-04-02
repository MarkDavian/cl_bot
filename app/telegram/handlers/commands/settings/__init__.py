from aiogram import Dispatcher

from .cmd_settings import cmd_settings
from .change_password import reg_settings_change_password
from .notify import reg_settings_notify
from .time_intervals import reg_intervals
from .time_to_notify import reg_settings_time_notify


def reg_settings(dp: Dispatcher):
    dp.register_message_handler(cmd_settings, commands="settings", state='*')
    reg_settings_change_password(dp)
    reg_settings_time_notify(dp)
    reg_settings_notify(dp)
    reg_intervals(dp)