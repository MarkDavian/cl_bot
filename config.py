"""
Модуль конфигурации приложения CL Bot.

Этот файл содержит настройки и конфигурационные параметры для работы бота.
Здесь определены константы времени, интервалы уведомлений, токены доступа
и другие параметры, необходимые для корректной работы приложения.
"""

from dataclasses import dataclass
import json


# Загрузка токена бота из файла
with open('.token', 'r') as file:
    env_token = file.readline()

# Загрузка идентификатора чата для отправки уведомлений
with open('.chat', 'r') as file:
    chat = file.readline()


# Загрузка настроек по умолчанию из JSON-файла
with open('storage/default_app.json', 'r') as file:
    default = json.load(file)
    
    
class Settings():
    """
    Класс основных настроек приложения.
    
    Содержит токен бота Telegram, идентификатор основного чата
    и константы для интервалов времени.
    """
    BOT_TOKEN: str = env_token
    CHAT: str = chat
    # 24 hours in seconds
    INTERVAL_24 = 24*60*60


@dataclass(frozen=True)
class STANDART_APP_SETTINGS():
    """
    Класс стандартных настроек приложения, загружаемых из JSON-файла.
    
    Атрибуты:
        PASSWORD (str): Пароль для доступа к боту
        LMK_NOTIFY_TIME_INTERVAL (int): Интервал проверки медицинских книжек в секундах
        DR_NOTIFY_TIME_INTERVAL (int): Интервал проверки дней рождения в секундах
        ANNIVERSARY_TIME_INTERVAL (int): Интервал проверки юбилеев в секундах
        CERTS_TIME_INTERVAL (int): Интервал проверки сертификатов в секундах
        TIME_TO_NOTIFY (str): Время отправки уведомлений в формате ЧЧ:ММ
    """
    PASSWORD: str = default['password']
    LMK_NOTIFY_TIME_INTERVAL: int = default['lmk_notify_time_interval']
    DR_NOTIFY_TIME_INTERVAL: int = default['dr_notify_time_interval']
    ANNIVERSARY_TIME_INTERVAL: int = default['anniversary_time_interval']
    CERTS_TIME_INTERVAL: int = default['certs_time_interval']
    TIME_TO_NOTIFY: str = default['time_to_notify']


# Экземпляр класса настроек для использования в других модулях
SETTINGS = Settings()

# Словарь допустимых интервалов для настройки периодичности уведомлений
ALLOWED_INTERVALS = {
    '12 часов': 12*60*60,
    '24 часа': 24*60*60,
    '2 дня': 24*2*60*60,
    '3 дня': 24*3*60*60,
    '4 дня': 24*4*60*60,
    '5 дней': 24*5*60*60,
    '1 неделя': 24*7*60*60
}

# Словарь допустимых значений времени для отправки уведомлений
ALLOWED_TIME_NOTIFY = {
    '8:00': '8:00',
    '9:00': '9:00',
    '10:00': '10:00',
    '11:00': '11:00',
    '12:00': '12:00',
    '13:00': '13:00',
    '14:00': '14:00',
    '15:00': '15:00',
    '16:00': '16:00',
    '17:00': '17:00',
    '18:00': '18:00',
    '19:00': '19:00',
    '20:00': '20:00',
    '21:00': '21:00',
    '22:00': '22:00',
    '23:00': '23:00'
}