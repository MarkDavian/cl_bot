from app.core.types.types import EmployeeBuilder
from app.core.db.database import Storage


def func_add_employee(
        name,
        birthday,
        registration,
        workstarted,
        lmk,
        id = None
):
    with Storage() as storage:
        storage.add(
            EmployeeBuilder(
                name,
                birthday,
                registration,
                workstarted,
                lmk,
                id
            ).__dict__()
        )