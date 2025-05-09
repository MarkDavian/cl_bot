from app.core.types.types import Employee, EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees


def check_anniversary() -> list[Employee]:
    employees = func_get_employees()
    anniversary = []
    for employee in employees:
        if (
            employee.get_days_to_anniversary() != 'Неизвестно' and employee.get_days_to_anniversary() < 30
        ):
            anniversary.append(employee)
        
    return anniversary