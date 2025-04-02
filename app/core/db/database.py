"""
Модуль базы данных приложения.

Этот модуль обеспечивает работу с локальными хранилищами данных,
реализованными в виде JSON-файлов. Модуль предоставляет классы для
управления различными типами данных: основное хранилище сотрудников,
данные пользователей и настройки приложения.
"""

import json
from bson import ObjectId


class Storage:
    """
    Класс для работы с основным хранилищем данных сотрудников.
    
    Обеспечивает чтение, запись, добавление и удаление записей
    из файла storage/storage.json, который содержит всю информацию
    о сотрудниках организации.
    
    Attributes:
        storage (dict): Словарь с данными из файла storage.json
    """
    storage: dict


    def __init__(self) -> None:
        """
        Инициализирует объект хранилища, считывая данные из файла.
        """
        with open('storage/storage.json', 'r') as file:
            self.storage = json.load(file)

    def __enter__(self):
        """
        Метод контекстного менеджера для использования с оператором with.
        
        Returns:
            Storage: Экземпляр объекта хранилища
        """
        return self
    
    def __exit__(self, type, value, traceback):
        """
        Метод контекстного менеджера для сохранения данных при выходе из контекста.
        
        Автоматически записывает изменения в файл при завершении блока with.
        
        Args:
            type: Тип исключения, если оно возникло
            value: Значение исключения
            traceback: Трассировка исключения
        """
        with open('storage/storage.json', 'w') as file: 
            json.dump(self.storage, file, indent=2, ensure_ascii=False)

    def get(self):
        """
        Получает все записи из хранилища.
        
        Returns:
            list: Список всех записей сотрудников
        """
        return self.storage['all']
    
    def get_by_id(self, id: str):
        """
        Находит запись сотрудника по его идентификатору.
        
        Args:
            id (str): Идентификатор сотрудника
            
        Returns:
            dict or None: Данные сотрудника или None, если сотрудник не найден
        """
        for c, item in enumerate(self.storage['all']):
            if item['id'] == id:
                return item

    def add(self, data: dict):
        """
        Добавляет новую запись в хранилище.
        
        Если у записи нет идентификатора, генерирует новый ObjectId.
        
        Args:
            data (dict): Данные сотрудника для добавления
            
        Returns:
            str: Идентификатор добавленной записи
        """
        id = data.get('id')
        if id is None:
            id = str(ObjectId())
            data['id'] = id
        self.storage['all'].append(data)
        return id
    
    def bulk_add(self, sequence: list[dict]):
        """
        Добавляет несколько записей в хранилище.
        
        Args:
            sequence (list[dict]): Список данных сотрудников
        """
        for data in sequence:
            self.add(data)

    def delete(self, id: str):
        """
        Удаляет запись из хранилища по идентификатору.
        
        Args:
            id (str): Идентификатор записи для удаления
        """
        for c, item in enumerate(self.storage['all']):
            if item['id'] == id:
                self.storage['all'].pop(c)


class Users:
    """
    Класс для работы с хранилищем данных пользователей.
    
    Обеспечивает чтение, запись, добавление и удаление записей
    из файла storage/users.json, который содержит информацию
    о пользователях системы, имеющих доступ к функциям бота.
    
    Attributes:
        storage (dict): Словарь с данными из файла users.json
    """
    storage: dict


    def __init__(self) -> None:
        """
        Инициализирует объект хранилища пользователей, считывая данные из файла.
        """
        with open('storage/users.json', 'r') as file:
            self.storage = json.load(file)

    def __enter__(self):
        """
        Метод контекстного менеджера для использования с оператором with.
        
        Returns:
            Users: Экземпляр объекта хранилища пользователей
        """
        return self
    
    def __exit__(self, type, value, traceback):
        """
        Метод контекстного менеджера для сохранения данных при выходе из контекста.
        
        Автоматически записывает изменения в файл при завершении блока with.
        
        Args:
            type: Тип исключения, если оно возникло
            value: Значение исключения
            traceback: Трассировка исключения
        """
        with open('storage/users.json', 'w') as file: 
            json.dump(self.storage, file, indent=2, ensure_ascii=False)

    def get(self):
        """
        Получает всех пользователей из хранилища.
        
        Returns:
            list: Список всех записей пользователей
        """
        return self.storage['all']
    
    def get_by_id(self, id: str):
        """
        Находит запись пользователя по его идентификатору.
        
        Args:
            id (str): Идентификатор пользователя
            
        Returns:
            dict or None: Данные пользователя или None, если пользователь не найден
        """
        for с, item in enumerate(self.storage['all']):
            if item['id'] == id:
                return item

    def add(self, data: dict):
        """
        Добавляет нового пользователя в хранилище.
        
        Если у записи нет идентификатора, генерирует новый ObjectId.
        
        Args:
            data (dict): Данные пользователя для добавления
            
        Returns:
            str: Идентификатор добавленного пользователя
        """
        id = data.get('id')
        if id is None:
            id = str(ObjectId())
            data['id'] = id
        self.storage['all'].append(data)
        return id
    
    def bulk_add(self, sequence: list[dict]):
        """
        Добавляет несколько пользователей в хранилище.
        
        Args:
            sequence (list[dict]): Список данных пользователей
        """
        for data in sequence:
            self.add(data)

    def delete(self, id: str):
        """
        Удаляет пользователя из хранилища по идентификатору.
        
        Args:
            id (str): Идентификатор пользователя для удаления
        """
        for c, item in enumerate(self.storage['all']):
            if item['id'] == id:
                self.storage['all'].pop(c)


class AppSettings:
    """
    Класс для работы с настройками приложения.
    
    Обеспечивает чтение и запись настроек приложения из файла storage/app.json,
    который содержит конфигурационные параметры системы, такие как пароли,
    интервалы уведомлений и другие параметры.
    
    Attributes:
        storage (dict): Словарь с настройками из файла app.json
    """
    storage: dict


    def __init__(self) -> None:
        """
        Инициализирует объект настроек приложения, считывая данные из файла.
        """
        with open('storage/app.json', 'r') as file:
            self.storage = json.load(file)

    def __enter__(self):
        """
        Метод контекстного менеджера для использования с оператором with.
        
        Returns:
            AppSettings: Экземпляр объекта настроек приложения
        """
        return self
    
    def __exit__(self, type, value, traceback):
        """
        Метод контекстного менеджера для сохранения данных при выходе из контекста.
        
        Автоматически записывает изменения в файл при завершении блока with.
        
        Args:
            type: Тип исключения, если оно возникло
            value: Значение исключения
            traceback: Трассировка исключения
        """
        with open('storage/app.json', 'w') as file: 
            json.dump(self.storage, file, indent=2, ensure_ascii=False)

    def get(self) -> dict:
        """
        Получает все настройки приложения.
        
        Returns:
            dict: Словарь всех настроек приложения
        """
        return self.storage

    def get_password(self):
        """
        Получает пароль от приложения.
        
        Returns:
            str: Пароль администратора приложения
        """
        return self.storage['password']
    
    def set_password(self, text: str):
        """
        Устанавливает новый пароль для приложения.
        
        Args:
            text (str): Новый пароль
            
        Returns:
            str: Установленный пароль
        """
        self.storage['password'] = text
        return text
    
    def get_dr_interval(self):
        """
        Получает интервал проверки дней рождения.
        
        Returns:
            int: Интервал в секундах
        """
        return self.storage['dr_interval']
    
    def set_dr_interval(self, seconds: int):
        """
        Устанавливает интервал проверки дней рождения.
        
        Args:
            seconds (int): Интервал в секундах
            
        Returns:
            int: Установленный интервал
        """
        self.storage['dr_interval'] = seconds
        return seconds
    
    def get_lmk_interval(self):
        """
        Получает интервал проверки ЛМК (личных медицинских книжек).
        
        Returns:
            int: Интервал в секундах
        """
        return self.storage['lmk_interval']
    
    def set_lmk_interval(self, seconds: int):
        """
        Устанавливает интервал проверки ЛМК.
        
        Args:
            seconds (int): Интервал в секундах
            
        Returns:
            int: Установленный интервал
        """
        self.storage['lmk_interval'] = seconds
        return seconds