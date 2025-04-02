from app.core.db.espresso_machines import EspressoMachinesDB
from datetime import datetime


def func_get_espresso_gasket_replacement_date() -> str:
    """Получает дату следующей замены резинок"""
    db = EspressoMachinesDB()
    machines = db.get_machines_needing_gasket_replacement()
    
    if not machines:
        return "✅ Все в порядке"
        
    message = "".join([
        f"📍 {machine.location}\n"
        f"📝 Модель: {machine.model}\n"
        f"🔄 Последняя замена: {machine.last_gasket_replacement}\n"
        f"⏰ Следующая замена: {machine.next_gasket_replacement}\n\n"
        for machine in machines
    ])
    
    return message


def func_get_espresso_health_bar() -> str:
    """Создает текстовый прогресс-бар здоровья кофемашин"""
    db = EspressoMachinesDB()
    machines = db.get_all_machines()
    
    if not machines:
        return "Нет данных о кофемашинах"
        
    total_health = 0
    for machine in machines:
        if not machine.next_gasket_replacement:
            continue
            
        next_date = datetime.strptime(machine.next_gasket_replacement, "%d.%m.%Y")
        current_date = datetime.now()
        
        # Если дата замены уже прошла
        if current_date >= next_date:
            total_health += 0
            continue
            
        # Вычисляем процент здоровья (180 дней = 100%)
        days_left = (next_date - current_date).days
        health_percentage = min(100, max(0, (days_left / 180) * 100))
        total_health += health_percentage
    
    # Среднее здоровье всех машин
    avg_health = total_health / len(machines)
    
    # Создаем прогресс-бар (20 символов)
    bar_length = 20
    filled_length = int(bar_length * avg_health / 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    return f"{bar}\n{avg_health:.1f}%" 