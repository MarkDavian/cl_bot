from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsSG(StatesGroup):
    start = State()
    change_password_start = State()

    intervals_start = State()
    change_interval = State()
    accept_interval = State()

    time_notify_start = State()
    time_notify_change = State()
    accept_time_notify = State()

    time_start = State()