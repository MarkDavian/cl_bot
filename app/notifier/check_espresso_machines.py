from app.core.db.espresso_machines import EspressoMachinesDB
from app.core.types.espresso_machine import EspressoMachine


def check_espresso_machines() -> list[EspressoMachine]:
    """
    Проверяет все кофемашины на необходимость замены резинок
    
    Returns:
        list[EspressoMachine]: Список кофемашин, требующих замены резинок
    """
    db = EspressoMachinesDB()
    return db.get_machines_needing_gasket_replacement()


def format_notification_message(machines: list[EspressoMachine]) -> str:
    """
    Форматирует сообщение для уведомления
    
    Args:
        machines: Список кофемашин, требующих замены резинок
        
    Returns:
        str: Отформатированное сообщение
    """
    if not machines:
        return ""
        
    message = "⚠️ Требуется замена резинок-уплотнителей в следующих кофемашинах:\n\n"
    
    for machine in machines:
        message += f"📍 {machine.location}\n"
        message += f"📝 Модель: {machine.model}\n"
        message += f"🔄 Последняя замена: {machine.last_gasket_replacement}\n"
        message += f"⏰ Следующая замена: {machine.next_gasket_replacement}\n\n"
        
    return message 