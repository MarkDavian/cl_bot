from app.core.db.database import Storage


def func_del_emp(id: str):
    with Storage() as s:
        emp = s.get_by_id(id)
        s.delete(id)

    return emp