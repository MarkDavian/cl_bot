from app.core.types.types import Employee, EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees


def check_lmk() -> list[Employee]:
    """
    Проверяет сотрудников на наличие просроченных медицинских книжек.

    Returns:
        list[Employee]: Список сотрудников с просроченными медицинскими книжками.
        Возвращает пустой список, если таких сотрудников нет.
    """
    employees = func_get_employees()
    lmk = []
    for employee in employees:
        if employee.needing_lmk_replacement():
            lmk.append(employee)
        
    return lmk


def check_exp_lmk() -> list[Employee]:
    """
    Проверяет сотрудников, у которых срок действия медицинской книжки истекает в ближайшие 30 дней.

    Returns:
        list[Employee]: Список сотрудников, у которых срок действия медицинской книжки 
        истекает в ближайшие 30 дней. Возвращает пустой список, если таких сотрудников нет.
    """
    employees = func_get_employees()
    lmk = []
    for employee in employees:
        time_to_lmk_replacement = employee.time_to_lmk_replacement()
        if employee.needing_lmk_replacement():
            continue
        if time_to_lmk_replacement != 'Неизвестно' and time_to_lmk_replacement < 31:
            lmk.append(employee)
        
    return lmk