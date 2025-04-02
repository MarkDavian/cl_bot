from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from bson import ObjectId


@dataclass
class ServiceDate:
    date: str
    description: str
    authorized: str = None
    _id: str = None

    def __post_init__(self):
        if self._id is None:
            self._id = str(ObjectId())


@dataclass
class EspressoMachine:
    id: str
    location: str
    model: str
    service_dates: List[ServiceDate]
    last_gasket_replacement: str
    next_gasket_replacement: str

    def __dict__(self):
        return {
            "id": self.id,
            "location": self.location,
            "model": self.model,
            "service_dates": [
                {
                    "date": sd.date,
                    "description": sd.description,
                    "authorized": sd.authorized,
                    "_id": sd._id
                } for sd in self.service_dates
            ],
            "last_gasket_replacement": self.last_gasket_replacement,
            "next_gasket_replacement": self.next_gasket_replacement
        }

    @classmethod
    def from_dict(cls, data: dict):
        service_dates = [ServiceDate(**sd) for sd in data.get("service_dates", [])]
        return cls(
            id=data["id"],
            location=data["location"],
            model=data["model"],
            service_dates=service_dates,
            last_gasket_replacement=data["last_gasket_replacement"],
            next_gasket_replacement=data["next_gasket_replacement"]
        )

    def add_service_date(self, 
        date: str, 
        description: str,
        authorized: str,
        _id: str = None,
    ) -> None:
        self.service_dates.append(ServiceDate(date=date, description=description, authorized=authorized, _id=_id))

    def update_gasket_replacement(self, date: str):
        self.last_gasket_replacement = date
        # Рассчитываем следующую замену через 6 месяцев
        next_date = datetime.strptime(date, "%d.%m.%Y")
        next_date = next_date.replace(month=next_date.month + 6)
        self.next_gasket_replacement = next_date.strftime("%d.%m.%Y")

    def needs_gasket_replacement(self) -> bool:
        """Проверяет, нужна ли замена резинок"""
        if not self.next_gasket_replacement:
            return False
            
        next_date = datetime.strptime(self.next_gasket_replacement, "%d.%m.%Y")
        current_date = datetime.now()

        print(current_date, next_date)
        
        return current_date >= next_date 