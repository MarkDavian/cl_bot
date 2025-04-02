from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from app.telegram.handlers.commands.settings.states import SettingsSG

from app.telegram.handlers.commands.settings.cmd_settings import cmd_settings
from app.telegram.handlers.commands.settings.time_intervals.intervals import reply_intervals_menu

from app.telegram.handlers.commands.settings.time_intervals.intervals import change_interval, interval_choosen, interval_accept


def reg_intervals(dp: Dispatcher):
    dp.register_message_handler(reply_intervals_menu, Text(equals='интервалы сообщений', ignore_case=True), state=SettingsSG.start.state)
    dp.register_message_handler(cmd_settings, Text(equals='назад', ignore_case=True), state=SettingsSG.intervals_start.state)

    dp.register_message_handler(change_interval, state=SettingsSG.intervals_start.state)
    dp.register_message_handler(reply_intervals_menu, Text(equals='назад', ignore_case=True), state=SettingsSG.change_interval.state)

    dp.register_message_handler(interval_choosen, state=SettingsSG.change_interval.state)
    dp.register_message_handler(interval_accept, state=SettingsSG.accept_interval.state)