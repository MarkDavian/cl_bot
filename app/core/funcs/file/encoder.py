from datetime import datetime


def uniq_name() -> str:
    """
    Генерирует уникальное имя файла с текущей датой и временем
    
    Returns:
        str: Имя файла в формате CRT_ДД.ММ.ГГГГ_ЧЧ:ММ:СС
    """
    current_time = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
    return f'CRT_{current_time}'