from app.core.db.database import Storage
from app.core.types.types import EmployeeBuilder

from app.core.types.types import Employee


def func_get_employees() -> list[Employee]:
    with Storage() as s:
        emps_dict = s.get()

    emps_obj = []
    for emp in emps_dict:
        emps_obj.append(EmployeeBuilder(**emp).get_employee())

    return emps_obj


def func_get_by_id(id) -> Employee:
    with Storage() as s:
        emp_dict = s.get_by_id(id)

    return EmployeeBuilder(**emp_dict).get_employee()
