"""
Модуль функций для добавления нового сотрудника.

Этот модуль предоставляет функцию для создания и сохранения
записи о новом сотруднике в хранилище данных. Функция
принимает все необходимые параметры сотрудника и использует
EmployeeBuilder для формирования объекта перед сохранением.
"""

from app.core.types.types import EmployeeBuilder
from app.core.db.database import Storage


def func_add_employee(
        name,
        birthday,
        registration,
        workstarted,
        lmk,
        id = None,
        cert_base = None,
        cert_base_path = [],
        cert_profi = None,
        cert_profi_path = [],
        test_results = []
):
    """
    Создает и сохраняет нового сотрудника в хранилище данных.
    
    Функция принимает все необходимые параметры для создания 
    нового сотрудника, формирует объект с помощью EmployeeBuilder 
    и сохраняет его в хранилище Storage.
    
    Args:
        name (str): ФИО сотрудника
        birthday (str): Дата рождения в формате ДД.ММ.ГГГГ
        registration (str): Дата регистрации в системе
        workstarted (str): Дата начала работы
        lmk (str): Дата оформления/обновления личной медицинской книжки
        id (str, optional): Идентификатор сотрудника. По умолчанию None (генерируется автоматически)
        cert_base (str, optional): Дата получения базового сертификата. По умолчанию None
        cert_base_path (list, optional): Пути к файлам базового сертификата. По умолчанию []
        cert_profi (str, optional): Дата получения профессионального сертификата. По умолчанию None
        cert_profi_path (list, optional): Пути к файлам профессионального сертификата. По умолчанию []
        test_results (list, optional): Список результатов тестирования. По умолчанию []
    
    Returns:
        None
    """
    with Storage() as storage:
        storage.add(
            EmployeeBuilder(
                name,
                birthday,
                registration,
                workstarted,
                lmk,
                id,
                cert_base,
                cert_base_path,
                cert_profi,
                cert_profi_path,
                test_results
            ).__dict__()
        )