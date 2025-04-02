"""
Модуль определения класса сотрудника и связанных с ним типов данных.

Этот модуль предоставляет основную структуру данных для работы с информацией о сотрудниках
кофеен, включая персональные данные, даты медицинских книжек и сертификатов, а также
результаты тестирований. Модуль содержит классы для создания, хранения и обработки
всех данных, связанных с сотрудниками.
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from bson import ObjectId


@dataclass(frozen=True)
class _TimeConst():
    """
    Класс констант для работы с временем.
    
    Содержит константы для перевода минут, часов и суток в секунды.
    Используется для внутренних расчётов временных интервалов.
    """
    minute = 60
    hour = 60 * minute
    hours_24 = 24 * hour


class TestType:
    """
    Класс для определения типов тестирования сотрудников.
    
    Содержит константы для обозначения различных типов тестов,
    которые могут проходить сотрудники компании.
    """
    BASE = "База"
    PROFI = "Профи"


@dataclass
class TestResult:
    """
    Класс для хранения результатов одного тестирования.
    
    Attributes:
        completion_time (str): Время прохождения в формате "MM:SS"
        score (int): Количество баллов
        rank (int): Место в списке
        date (str): Дата прохождения теста в формате DD.MM.YYYY
        type (TestType): Тип теста
        _id (str): Уникальный идентификатор результата тестирования
    """
    completion_time: str
    score: int
    rank: int
    date: str
    type: TestType
    _id: str

    def __init__(
        self, 
        completion_time: str, 
        score: int, 
        rank: int, 
        date: str, 
        type: TestType, 
        _id: str = None
    ) -> None:
        """
        Инициализирует новый объект результата тестирования.
        
        Args:
            completion_time (str): Время прохождения теста
            score (int): Набранные баллы
            rank (int): Ранг/место в списке результатов
            date (str): Дата прохождения теста
            type (TestType): Тип пройденного теста
            _id (str, optional): Уникальный идентификатор. Если не указан, генерируется автоматически.
        """
        self.completion_time = completion_time
        self.score = score
        self.rank = rank
        self.date = date
        self.type = type
        if not _id:
            self._id = str(ObjectId())
        else:
            self._id = _id

    def __dict__(self):
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            dict: Словарь с атрибутами объекта
        """
        x = {
                "completion_time": self.completion_time,
                "score": self.score,
                "rank": self.rank,
                "date": self.date,
                "type": self.type,
        }
        if self._id:
            x["_id"] = self._id
        return x

class Employee():
    """
    Класс для представления сотрудника компании.

    Attributes:
        name (str): ФИО сотрудника
        birthday (str): Дата рождения в формате DD.MM.YYYY
        registration (str): Адрес регистрации
        workstarted (str): Дата начала работы в формате DD.MM.YYYY  
        lmk (str): Дата начала действия медицинской книжки в формате DD.MM.YYYY
        id (str): Уникальный идентификатор сотрудника
        cert_base (str): Дата начала действия базового сертификата в формате DD.MM.YYYY
        cert_base_path (list[str]): Список путей к файлам базовых сертификатов
        cert_profi (str): Дата начала действия профессионального сертификата в формате DD.MM.YYYY
        cert_profi_path (list[str]): Список путей к файлам профессиональных сертификатов
        test_results (list[TestResult]): Список результатов тестирований
    """
    name: str
    birthday: str
    registration: str
    experience: str
    workstarted: str
    lmk: str
    id: str
    cert_base: str
    cert_base_path: list[str]
    cert_profi: str
    cert_profi_path: list[str]
    test_results: List[TestResult]
    

    def __init__(self,
                name: str,
                birthday: str,
                registration: str,
                workstarted: str,
                lmk: str,
                id: str,
                cert_base: str = "",
                cert_base_path: list[str] = [],
                cert_profi: str = "",
                cert_profi_path: list[str] = [],
                test_results: List[TestResult] = None
        ) -> None:
        """
        Инициализирует новый объект сотрудника.
        
        Args:
            name (str): ФИО сотрудника
            birthday (str): Дата рождения в формате DD.MM.YYYY
            registration (str): Адрес регистрации
            workstarted (str): Дата начала работы в формате DD.MM.YYYY
            lmk (str): Дата начала действия медицинской книжки в формате DD.MM.YYYY
            id (str): Уникальный идентификатор сотрудника
            cert_base (str, optional): Дата начала действия базового сертификата
            cert_base_path (list[str], optional): Список путей к файлам базовых сертификатов
            cert_profi (str, optional): Дата начала действия профессионального сертификата
            cert_profi_path (list[str], optional): Список путей к файлам профессиональных сертификатов
            test_results (List[TestResult], optional): Список результатов тестирований
        """
        self.name = name
        self.birthday = birthday
        self.registration = registration
        self.workstarted = workstarted
        self.lmk = lmk
        self.id = id
        self.cert_base = cert_base
        self.cert_base_path = cert_base_path
        self.cert_profi = cert_profi
        self.cert_profi_path = cert_profi_path
        self.test_results = test_results or []


    def __dict__(self) -> dict:
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            dict: Словарь с атрибутами объекта
        """
        return {
            "name": self.name,
            "birthday": self.birthday,
            "registration": self.registration,
            "workstarted": self.workstarted,
            "lmk": self.lmk,
            "id": self.id,
            "cert_base": self.cert_base,
            "cert_base_path": self.cert_base_path,
            "cert_profi": self.cert_profi,
            "cert_profi_path": self.cert_profi_path,
            "test_results": [
                result.__dict__()
                for result in self.test_results
            ]
        }

    def get_experience(self) -> str:
        """
        Вычисляет стаж работы сотрудника.
        
        Returns:
            str: Стаж работы в формате "X лет Y месяцев Z дней"
        """
        try:
            workstarted_date = datetime.strptime(self.workstarted, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        experience_date = datetime.now() - workstarted_date

        years = experience_date.days // 365
        days = experience_date.days - (years*365)

        month = days // 30
        days = days - (month*30)

        years_postfix = "лет"
        month_postfix = "месяцев"
        days_postfix = "дней"
        if years == 0:
            years = ''
            years_postfix = ""
        elif years == 1:
            years_postfix = "год"
        elif years == 2 or years == 3 or years == 4:
            years_postfix = "года"

        if month == 0:
            month = ''
            month_postfix = ""
        elif month == 1:
            month_postfix = "месяц"
        elif month == 2 or month == 3 or month == 4:
            month_postfix = "месяца"

        if days == 0:
            days = ''
            days_postfix = ""
        elif days == 1 or list(str(days))[-1] == '1':
            days_postfix = "день"
        elif list(str(days))[0] != '1':
            if days == 2 or days == 3 or days == 4 or list(str(days))[-1] == '2' or list(str(days))[-1] == '3' or list(str(days))[-1] == '4':
                days_postfix = "дня"

        # Собираем только непустые значения
        parts = []
        if years:
            parts.append(f"{years} {years_postfix}")
        if month:
            parts.append(f"{month} {month_postfix}")
        if days:
            parts.append(f"{days} {days_postfix}")
            
        return " ".join(parts)

    def get_lmk_expire_date(self):
        """
        Вычисляет дату окончания действия медицинской книжки.
        
        Returns:
            str: Дата окончания действия медицинской книжки в формате DD.MM.YYYY
        """
        lmk_date = datetime.strptime(self.lmk, '%d.%m.%Y')
        lmk_expiry = lmk_date.replace(year=lmk_date.year + 1)
        return lmk_expiry.strftime('%d.%m.%Y')
    
    def get_days_to_birth(self):
        """
        Вычисляет количество дней до дня рождения сотрудника.
        
        Returns:
            str: Количество дней до дня рождения сотрудника
        """
        try:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        return self._calculate_dates(birthday, now)
    
    def get_days_to_anniversary(self):
        """
        Вычисляет количество дней до годовщины начала работы сотрудника.
        
        Returns:
            str: Количество дней до годовщины начала работы сотрудника
        """
        try:
            anniversary = datetime.strptime(self.workstarted, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        return self._calculate_dates(anniversary, now)

    def get_days_to_cert(self, cert_type: str):
        """
        Вычисляет количество дней до окончания действия сертификата.
        
        Args:
            cert_type (str): Тип сертификата ('base' или 'profi')
        
        Returns:
            str: Количество дней до окончания действия сертификата
        """
        if cert_type.lower() == 'base' or cert_type.lower() == 'база':
            cert = self.cert_base
        else:
            cert = self.cert_profi

        try:
            replacement_date = datetime.strptime(cert, '%d.%m.%Y') + timedelta(days=365)
            now = datetime.now()
            return (replacement_date - now).days
        except Exception as e:
            return "Отсутствует"

    def get_cert_expire_date(self, cert_type: str):
        """
        Вычисляет дату окончания действия сертификата.
        
        Args:
            cert_type (str): Тип сертификата ('base' или 'profi')
        
        Returns:
            str: Дата окончания действия сертификата в формате DD.MM.YYYY
        """
        if cert_type.lower() == 'base' or cert_type.lower() == 'база':
            cert = self.cert_base
        else:
            cert = self.cert_profi

        try:
            replacement_date = datetime.strptime(cert, '%d.%m.%Y') + timedelta(days=365)
            return replacement_date.strftime('%d.%m.%Y')
        except Exception as e:
            return "Отсутствует"

    def get_cert_by_type(self, cert_type: str):
        """
        Возвращает список путей к файлам сертификата.
        
        Args:
            cert_type (str): Тип сертификата ('base' или 'profi')
        
        Returns:
            list[str]: Список путей к файлам сертификата
        """
        if cert_type.lower() == 'base' or cert_type.lower() == 'база':
            return self.cert_base_path
        else:
            return self.cert_profi_path

    def needing_cert_replacement(self, cert_type: str):
        """
        Проверяет, требуется ли замена сертификата.
        
        Args:
            cert_type (str): Тип сертификата ('base' или 'profi')
        
        Returns:
            bool: True если сертификат просрочен, False в противном случае
        """
        try:
            cert_date = datetime.strptime(self.get_cert_by_type(cert_type), '%d.%m.%Y')
            expiration_date = cert_date + timedelta(days=365)
            if datetime.now() > expiration_date:
                return True
        except Exception as e:
            pass
        return False

    def get_days_lmk(self):
        """
        Вычисляет количество дней до окончания действия медицинской книжки.
        
        Returns:
            str: Количество дней до окончания действия медицинской книжки
        """
        try:
            lmk = datetime.strptime(self.lmk, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        return self._calculate_dates(lmk, now)
    
    def needing_lmk_replacement(self):
        """
        Проверяет, требуется ли замена медицинской книжки.
        
        Returns:
            bool: True если медицинская книжка просрочена, False в противном случае
        """
        try:
            lmk_date = datetime.strptime(self.lmk, '%d.%m.%Y')
            expiration_date = lmk_date + timedelta(days=365)
            if datetime.now() > expiration_date:
                return True
        except ValueError as e:
            pass
        return False

    def time_to_lmk_replacement(self):
        """
        Вычисляет количество дней до замены медицинской книжки.
        
        Returns:
            Union[int, str]: Количество дней до замены медицинской книжки
        """
        try:
            lmk_date = datetime.strptime(self.lmk, '%d.%m.%Y')
            replacement_date = lmk_date + timedelta(days=365)
            now = datetime.now()
            return (replacement_date - now).days
        except ValueError:
            return "Неизвестно"
        
    def _calculate_dates(self, original_date, now):
        """
        Вычисляет количество дней до определенной даты.
        
        Args:
            original_date (datetime): Дата, до которой необходимо вычислить количество дней
            now (datetime): Текущая дата
        
        Returns:
            int: Количество дней до определенной даты
        """
        delta1 = datetime(now.year, original_date.month, original_date.day)
        delta2 = datetime(now.year+1, original_date.month, original_date.day)
        
        return ((delta1 if delta1 > now else delta2) - now).days
    
    def get_years_old(self):
        """
        Вычисляет возраст сотрудника.
        
        Returns:
            str: Возраст сотрудника
        """
        try:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        years = now.year - birthday.year
        
        # Корректировка возраста если день рождения в этом году еще не наступил
        if now.month < birthday.month or (now.month == birthday.month and now.day < birthday.day):
            years -= 1
            
        return years

    def add_test_result(self, test_result: TestResult) -> None:
        """
        Добавляет результат тестирования.
        
        Args:
            test_result (TestResult): Результат тестирования
        """
        self.test_results.append(test_result)

    def find_test_result(self, _id: str) -> TestResult:
        """
        Находит результат тестирования по идентификатору.
        
        Args:
            _id (str): Идентификатор результата тестирования
        
        Returns:
            TestResult: Результат тестирования или None если не найден
        """
        for result in self.test_results:
            if result._id == _id:
                return result
        return None


class EmployeeBuilder():
    """
    Класс для построения объекта сотрудника.
    """
    def __init__(self,
                name: str = "",
                birthday: str = "",
                registration: str = "",
                workstarted: str = "",
                lmk: str = "",
                id: str = "",
                cert_base: str = "",
                cert_base_path: list[str] = [],
                cert_profi: str = "",
                cert_profi_path: list[str] = [],
                test_results: List[TestResult] = []
        ) -> None:
        """
        Инициализирует новый объект построителя сотрудника.
        
        Args:
            name (str): ФИО сотрудника
            birthday (str): Дата рождения в формате DD.MM.YYYY
            registration (str): Адрес регистрации
            workstarted (str): Дата начала работы в формате DD.MM.YYYY
            lmk (str): Дата начала действия медицинской книжки в формате DD.MM.YYYY
            id (str): Уникальный идентификатор сотрудника
            cert_base (str, optional): Дата начала действия базового сертификата
            cert_base_path (list[str], optional): Список путей к файлам базовых сертификатов
            cert_profi (str, optional): Дата начала действия профессионального сертификата
            cert_profi_path (list[str], optional): Список путей к файлам профессиональных сертификатов
            test_results (List[TestResult], optional): Список результатов тестирований
        """
        try:
            if len(test_results) != 0:
                if type(test_results[0]) == dict:
                    x = []
                    for result in test_results:
                        x.append(TestResult(
                            completion_time=result['completion_time'],
                            score=result['score'],
                            rank=result['rank'],
                            date=result['date'],
                            type=result['type'],
                            _id=result['_id']
                        ))
                    test_results = x
        except Exception as e:
            pass
        self.employee = Employee(
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
        )
    
    def get_employee(self):
        """
        Возвращает построенный объект сотрудника.
        
        Returns:
            Employee: Построенный объект сотрудника
        """
        return self.employee
    
    def __dict__(self):
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            dict: Словарь с атрибутами объекта
        """
        return self.employee.__dict__()