from app.core.types.types import Employee, EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees


def check_lmk() -> list[Employee]:
    employees = func_get_employees()
    lmk = []
    for employee in employees:
        days_to_lmk = employee.get_days_lmk()
        if (
            days_to_lmk != 'Неизвестно' and days_to_lmk < 6*31
        ):
            lmk.append(employee)
        
    return lmk