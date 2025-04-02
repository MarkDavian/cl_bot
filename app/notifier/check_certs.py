from app.core.types.types import Employee, EmployeeBuilder
from app.core.funcs.get_employees import func_get_employees


def check_certs() -> list[tuple[Employee, str]]:
    """
    Проверяет сотрудников на наличие просроченных медицинских книжек.

    Returns:
        list[tuple[Employee]: Список сотрудников с просроченными медицинскими книжками.
        Возвращает пустой список, если таких сотрудников нет.
    """
    employees = func_get_employees()
    data = []
    for employee in employees:
        for cert_type in ['база', 'профи']:
            if employee.needing_cert_replacement(cert_type):
                data.append((employee, cert_type))
        
    return data


def check_exp_certs() -> list[tuple[Employee, str]]:
    """
    Проверяет сотрудников, у которых срок действия медицинской книжки истекает в ближайшие 30 дней.

    Returns:
        list[tuple[Employee, str]]: Список сотрудников, у которых срок действия медицинской книжки 
        истекает в ближайшие 30 дней. Возвращает пустой список, если таких сотрудников нет.
    """
    employees = func_get_employees()
    data = []
    for employee in employees:
        for cert_type in ['база', 'профи']:
            if employee.needing_cert_replacement(cert_type):
                continue
            time_to_cert_replacement = employee.get_days_to_cert(cert_type)
            if time_to_cert_replacement != 'Отсутствует' and time_to_cert_replacement < 31:
                data.append((employee, cert_type))
        
    return data