"""
Модуль определения класса приложения и связанных с ним типов данных.

Этот модуль содержит класс App, который управляет основными настройками приложения,
такими как пароли, интервалы уведомлений и время отправки сообщений.
Здесь определены все типы данных для работы с настройками и их сохранением.
"""

from enum import Enum
from dataclasses import dataclass

from config import STANDART_APP_SETTINGS

from app.core.db.database import AppSettings


# class TimeInterval(int):
#     def to_str_date(self) --> str:
#         for key, val in allowed_intervals.items():
#             if val == value:
#                 return key


# class CHANGEABLES: 
#     password: str
#     lmk_notify_time_interval: TimeInterval
#     dr_notify_time_interval: TimeInterval
#     anniversary_time_interval: TimeInterval
#     time_to_notify: str


class IntervalType(Enum):
    """
    Перечисление типов интервалов уведомлений.
    
    Определяет константы для различных типов уведомлений, 
    позволяя единообразно обращаться к ним в коде.
    """
    DR = 'DR'               # Интервал проверки дней рождения
    LMK = 'LMK'             # Интервал проверки медицинских книжек
    ANNIVERSARY = 'ANNIVERSARY'  # Интервал проверки юбилеев
    CERTS = 'CERTS'         # Интервал проверки сертификатов


@dataclass(frozen=True)
class Interval:
    """
    Класс для хранения информации об интервале уведомлений.
    
    Связывает тип интервала с текстом кнопки для его изменения
    в пользовательском интерфейсе.
    
    Attributes:
        type (IntervalType): Тип интервала уведомлений
        button_txt (str): Текст кнопки для изменения данного интервала
    """
    type: IntervalType
    button_txt: str


@dataclass(frozen=True)
class NAMED_INTERVALS:
    """
    Класс, содержащий предопределенные именованные интервалы.
    
    Предоставляет набор констант и методы для работы с различными 
    типами интервалов уведомлений и их представлением в интерфейсе.
    """
    dr = Interval(type=IntervalType.DR, button_txt='Изменить ДР')
    lmk = Interval(type=IntervalType.LMK, button_txt='Изменить ЛМК')
    anniversary = Interval(type=IntervalType.ANNIVERSARY, button_txt='Изменить ЮБИЛЕЙ')
    certs = Interval(type=IntervalType.CERTS, button_txt='Изменить Сертификаты')

    _button_to_interval = {
        dr.button_txt: dr,
        lmk.button_txt: lmk,
        anniversary.button_txt: anniversary,
        certs.button_txt: certs
    }

    @staticmethod
    def get_from_button(button: str) -> Interval:
        """
        Получает объект Interval по тексту кнопки.
        
        Args:
            button (str): Текст кнопки
            
        Returns:
            Interval: Объект интервала, соответствующий кнопке
        """
        return NAMED_INTERVALS._button_to_interval.get(button)


class App:
    """
    Класс, представляющий настройки приложения.
    
    Хранит и управляет всеми изменяемыми настройками приложения,
    такими как пароль и интервалы уведомлений, а также предоставляет
    методы для их сохранения.
    
    Attributes:
        password (str): Пароль для доступа к приложению
        lmk_notify_time_interval (int): Интервал проверки ЛМК в секундах
        dr_notify_time_interval (int): Интервал проверки дней рождения в секундах
        anniversary_time_interval (int): Интервал проверки юбилеев в секундах
        certs_time_interval (int): Интервал проверки сертификатов в секундах
        time_to_notify (str): Время отправки уведомлений в формате ЧЧ:ММ
    """
    password: str
    lmk_notify_time_interval: int
    dr_notify_time_interval: int
    anniversary_time_interval: int
    certs_time_interval: int
    time_to_notify: str

    def __init__(self,
                password: str,
                lmk_notify_time_interval: int,
                dr_notify_time_interval: int,
                anniversary_time_interval: int,
                certs_time_interval: int,
                time_to_notify: str,
    ) -> None:
        """
        Инициализирует объект настроек приложения.
        
        Args:
            password (str): Пароль для доступа к приложению
            lmk_notify_time_interval (int): Интервал проверки ЛМК в секундах
            dr_notify_time_interval (int): Интервал проверки дней рождения в секундах
            anniversary_time_interval (int): Интервал проверки юбилеев в секундах
            certs_time_interval (int): Интервал проверки сертификатов в секундах
            time_to_notify (str): Время отправки уведомлений в формате ЧЧ:ММ
        """
        self.password = password
        self.lmk_notify_time_interval = lmk_notify_time_interval
        self.dr_notify_time_interval = dr_notify_time_interval
        self.anniversary_time_interval = anniversary_time_interval
        self.certs_time_interval = certs_time_interval
        self.time_to_notify = time_to_notify

    def __dict__(self):
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            dict: Словарь с настройками приложения
        """
        return {
            "password": self.password,
            "lmk_notify_time_interval": self.lmk_notify_time_interval,
            "dr_notify_time_interval": self.dr_notify_time_interval,
            "anniversary_time_interval": self.anniversary_time_interval,
            "certs_time_interval": self.certs_time_interval,
            "time_to_notify": self.time_to_notify
        }

    def save(self):
        """
        Сохраняет настройки приложения в хранилище.
        
        Записывает текущие настройки в базу данных, чтобы они
        были доступны при следующем запуске приложения.
        """
        with AppSettings() as s:
            s.storage = self.__dict__()


class AppBuilder:
    """
    Класс для построения объекта настроек приложения.
    
    Упрощает создание объекта App с настройками по умолчанию
    или с переопределенными значениями.
    """
    def __init__(self,
                password: str = STANDART_APP_SETTINGS.PASSWORD,
                lmk_notify_time_interval: int = STANDART_APP_SETTINGS.LMK_NOTIFY_TIME_INTERVAL,
                dr_notify_time_interval: str = STANDART_APP_SETTINGS.DR_NOTIFY_TIME_INTERVAL,
                anniversary_time_interval: int = STANDART_APP_SETTINGS.ANNIVERSARY_TIME_INTERVAL,
                certs_time_interval: int = STANDART_APP_SETTINGS.CERTS_TIME_INTERVAL,
                time_to_notify: str = STANDART_APP_SETTINGS.TIME_TO_NOTIFY
    ) -> None:
        """
        Инициализирует построитель настроек приложения.
        
        Args:
            password (str, optional): Пароль для доступа к приложению
            lmk_notify_time_interval (int, optional): Интервал проверки ЛМК в секундах
            dr_notify_time_interval (int, optional): Интервал проверки дней рождения в секундах
            anniversary_time_interval (int, optional): Интервал проверки юбилеев в секундах
            certs_time_interval (int, optional): Интервал проверки сертификатов в секундах
            time_to_notify (str, optional): Время отправки уведомлений в формате ЧЧ:ММ
        """
        self.app = App(
            password,
            lmk_notify_time_interval,
            dr_notify_time_interval,
            anniversary_time_interval,
            certs_time_interval,
            time_to_notify
        )

    def get_app(self):
        """
        Возвращает построенный объект настроек приложения.
        
        Returns:
            App: Объект настроек приложения
        """
        return self.app

    def __dict__(self):
        """
        Преобразует объект построителя в словарь.
        
        Returns:
            dict: Словарь с настройками приложения
        """
        return self.app.__dict__()