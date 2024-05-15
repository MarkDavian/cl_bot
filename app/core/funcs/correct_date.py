from datetime import datetime


def is_date_correct(date: str):
    try:
        datetime.strptime(date, '%d.%m.%Y')
        return None
    except ValueError:
        return "Неправильный формат даты"