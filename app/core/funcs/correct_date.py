"""
Модуль функций для проверки и обработки дат и времени.

Этот модуль предоставляет набор утилит для проверки корректности
формата дат и времени, а также для преобразования временных интервалов
в удобный для человека формат. Используется во многих частях приложения
для валидации пользовательского ввода и форматирования отображения.
"""

import time
from datetime import datetime

from config import ALLOWED_INTERVALS


def date_incorrect(date: str):
    """
    Проверяет корректность формата даты.
    
    Функция пытается преобразовать строку в объект datetime 
    с форматом ДД.ММ.ГГГГ, и возвращает описание ошибки
    в случае некорректного формата.
    
    Args:
        date (str): Строка с датой для проверки
        
    Returns:
        str or None: Описание ошибки в случае некорректного формата,
                    None если формат даты корректен
    """
    try:
        datetime.strptime(date, '%d.%m.%Y')
        return None
    except ValueError:
        return "Неправильный формат даты"
    

def is_time_correct(user_time: str):
    """
    Проверяет корректность формата времени.
    
    Функция пытается преобразовать строку в объект time 
    с форматом ЧЧ:ММ, и возвращает описание ошибки
    в случае некорректного формата.
    
    Args:
        user_time (str): Строка с временем для проверки
        
    Returns:
        str or None: Описание ошибки в случае некорректного формата,
                    None если формат времени корректен
    """
    try:
        time.strptime(user_time, '%H:%M')
        return None
    except ValueError:
        return "Неправильный формат времени"
    

def humanize_date(value):
    """
    Преобразует числовое значение интервала в человекочитаемую строку.
    
    Функция находит ключ в словаре ALLOWED_INTERVALS,
    соответствующий переданному значению, что позволяет
    представить временной интервал в удобном для пользователя виде.
    
    Args:
        value (int): Числовое значение интервала
        
    Returns:
        str: Строковое представление интервала
    """
    for key, val in ALLOWED_INTERVALS.items():
        if val == value:
            return key
#     """
#     ДОДЕЛАТЬ !!!!!!!!!
#     """
#     try:
#         workstarted_date = datetime.strptime(self.workstarted, '%d.%m.%Y')
#     except ValueError:
#         return "Неизвестно"
    
#     experience_date = datetime.now() - workstarted_date

#     years = experience_date.days // 365
#     days = experience_date.days - (years*365)

#     month = days // 30
#     days = days - (month*30)

#     if years == 1:
#         years_postfix = "год"
#     elif years == 2 or years == 3 or years == 4:
#         years_postfix = "года"
#     else:
#         years_postfix = "лет"

#     if month == 1:
#         month_postfix = "месяц"
#     elif month == 2 or month == 3 or month == 4:
#         month_postfix = "месяца"
#     else:
#         month_postfix = "месяцев"

#     if days == 1 or list(str(days))[-1] == 1:
#         days_postfix = "день"
#     elif days == 2 or days == 3 or days == 4 or list(str(days))[-1] == 2 or list(str(days))[-1] == 3 or list(str(days))[-1] == 4:
#         days_postfix = "дня"
#     else:
#         days_postfix = "дней"

#     return f"{years} {years_postfix} {month} {month_postfix} {days} {days_postfix}"