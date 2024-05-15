from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuSG(StatesGroup):
    start = State()
    dates_diff = State()
    days_for = State()
    last_date = State()


class DatesDiffSG(StatesGroup):
    start = State()
    last_date = State()


class LastDateSG(StatesGroup):
    start = State()
    days = State()


class AddSG(StatesGroup):
    start = State()
    birthday = State()
    workstarted = State()
    lmk = State()
    end = State()


class EmployeesSG(StatesGroup):
    Choose = State()
    Employee = State()
    Change = State()
    Change_name = State()
    Change_birthday = State()
    Change_workstarted = State()
    Change_lmk = State()
    Delete = State()


class CurSG(StatesGroup):
    Choose = State()
    Employee = State()
