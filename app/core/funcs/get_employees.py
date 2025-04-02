"""
Модуль функций для получения данных о сотрудниках.

Этот модуль содержит функции для получения списка всех сотрудников
и поиска конкретного сотрудника по идентификатору. Функции преобразуют
данные из формата хранения (словари) в объекты типа Employee для
удобной работы с ними в остальных частях приложения.
"""

from app.core.db.database import Storage
from app.core.types import EmployeeBuilder, Employee, TestResult


def func_get_employees() -> list[Employee]:
    """
    Получает список всех сотрудников из хранилища данных.
    
    Функция считывает данные из хранилища, преобразует их из формата
    словарей в объекты типа Employee, включая результаты тестирования,
    которые преобразуются в объекты TestResult.
    
    Returns:
        list[Employee]: Список объектов сотрудников
    """
    with Storage() as s:
        emps_dict = s.get()

    emps_obj = []
    for emp in emps_dict:
        # Преобразуем результаты тестирования из словаря в объекты TestResult
        test_results = []
        if 'test_results' in emp:
            for result in emp['test_results']:
                test_results.append(TestResult(
                    completion_time=result['completion_time'],
                    score=result['score'],
                    rank=result['rank'],
                    date=result['date'],
                    type=result['type'],
                    _id=result['_id']
                ))
        
        # Создаем EmployeeBuilder с результатами тестирования
        builder = EmployeeBuilder(
            name=emp['name'],
            birthday=emp['birthday'],
            registration=emp['registration'],
            workstarted=emp['workstarted'],
            lmk=emp['lmk'],
            id=emp['id'],
            cert_base=emp.get('cert_base', ''),
            cert_base_path=emp.get('cert_base_path', []),
            cert_profi=emp.get('cert_profi', ''),
            cert_profi_path=emp.get('cert_profi_path', []),
            test_results=test_results
        )
        emps_obj.append(builder.get_employee())

    return emps_obj


def func_get_by_id(id) -> Employee:
    """
    Находит и возвращает сотрудника по его идентификатору.
    
    Функция ищет сотрудника в хранилище по указанному идентификатору,
    затем преобразует данные из формата словаря в объект типа Employee,
    включая результаты тестирования.
    
    Args:
        id (str): Идентификатор сотрудника
    
    Returns:
        Employee: Объект сотрудника
        
    Raises:
        ValueError: Если сотрудник с указанным идентификатором не найден
    """
    with Storage() as s:
        emp_dict = s.get_by_id(id)
        if emp_dict is None:
            raise ValueError(f"Сотрудник с id {id} не найден")
            
        # Преобразуем результаты тестирования из словаря в объекты TestResult
        test_results = []
        if 'test_results' in emp_dict:
            for result in emp_dict['test_results']:
                test_results.append(TestResult(
                    completion_time=result['completion_time'],
                    score=result['score'],
                    rank=result['rank'],
                    date=result['date'],
                    type=result['type'],
                    _id=result['_id']
                ))
        
        # Создаем EmployeeBuilder с результатами тестирования
        builder = EmployeeBuilder(
            name=emp_dict['name'],
            birthday=emp_dict['birthday'],
            registration=emp_dict['registration'],
            workstarted=emp_dict['workstarted'],
            lmk=emp_dict['lmk'],
            id=emp_dict['id'],
            cert_base=emp_dict.get('cert_base', ''),
            cert_base_path=emp_dict.get('cert_base_path', []),
            cert_profi=emp_dict.get('cert_profi', ''),
            cert_profi_path=emp_dict.get('cert_profi_path', []),
            test_results=test_results
        )
        return builder.get_employee()
