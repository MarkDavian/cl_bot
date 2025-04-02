import json
from typing import List, Optional
from bson import ObjectId

from app.core.types.espresso_machine import EspressoMachine


class EspressoMachinesDB:
    def __init__(self) -> None:
        """Инициализация базы данных"""
        self.file_path = 'storage/espresso_machines.json'
        self.machines: List[EspressoMachine] = []
        self._load_data()

    def __enter__(self):
        """Возвращает себя при использовании в качестве контекстного менеджера"""
        self._load_data()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Сохраняет данные при выходе из контекстного менеджера"""
        self._save_data()
        
    def _load_data(self) -> None:
        """Загрузка данных из файла"""
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.machines = [EspressoMachine.from_dict(machine) for machine in data]
        except FileNotFoundError:
            self.machines = []
            
    def _save_data(self) -> None:
        """Сохранение данных в файл"""
        with open(self.file_path, 'w') as file:
            json.dump([machine.__dict__() for machine in self.machines], file, indent=2, ensure_ascii=False)
            
    def add_machine(self, location: str, model: str) -> EspressoMachine:
        """
        Добавление новой кофемашины
        
        Args:
            location: Местоположение
            model: Модель
            
        Returns:
            EspressoMachine: Созданный объект кофемашины
        """
        machine = EspressoMachine(
            id=str(ObjectId()),
            location=location,
            model=model
        )
        self.machines.append(machine)
        self._save_data()
        return machine

    def add(self, machine: EspressoMachine) -> None:
        """
        Добавление кофемашины
        
        Args:
            machine: Объект кофемашины
        """
        self.machines.append(machine)
        self._save_data()
                
    def get_machine(self, machine_id: str) -> Optional[EspressoMachine]:
        """
        Получение кофемашины по ID
        
        Args:
            machine_id: ID кофемашины
            
        Returns:
            Optional[EspressoMachine]: Объект кофемашины или None
        """
        for machine in self.machines:
            if machine.id == machine_id:
                return machine
        return None
        
    def get_machines_by_location(self, location: str) -> List[EspressoMachine]:
        """
        Получение всех кофемашин в определенном месте
        
        Args:
            location: Местоположение
            
        Returns:
            List[EspressoMachine]: Список кофемашин
        """
        return [machine for machine in self.machines if machine.location == location]
        
    def get_all_machines(self) -> List[EspressoMachine]:
        """
        Получение всех кофемашин
        
        Returns:
            List[EspressoMachine]: Список всех кофемашин
        """
        return self.machines
        
    def update_machine(self, machine: EspressoMachine) -> None:
        """
        Обновление данных кофемашины
        
        Args:
            machine: Объект кофемашины с обновленными данными
        """
        for i, m in enumerate(self.machines):
            if m.id == machine.id:
                self.machines[i] = machine
                self._save_data()
                break
                
    def get_machines_needing_gasket_replacement(self) -> List[EspressoMachine]:
        """
        Получение списка кофемашин, требующих замены резинок
        
        Returns:
            List[EspressoMachine]: Список кофемашин
        """
        return [machine for machine in self.machines if machine.needs_gasket_replacement()] 

    def delete_machine(self, machine_id: str) -> None:
        """
        Удаление кофемашины по ID
        
        Args:
            machine_id: ID кофемашины
        """
        self.machines = [machine for machine in self.machines if machine.id != machine_id]