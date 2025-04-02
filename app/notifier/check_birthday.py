from app.core.types.types import Employee, EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees


def check_birthday() -> list[Employee]:
    employees = func_get_employees()
    dr = []
    for employee in employees:
        if (
            employee.get_days_to_birth() != 'Неизвестно' and employee.get_days_to_birth() < 10
        ):
            dr.append(employee)
        
    return dr