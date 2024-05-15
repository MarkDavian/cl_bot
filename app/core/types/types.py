from datetime import datetime


class Employee():
    name: str
    birthday: str
    registration: str
    experience: str
    workstarted: str
    lmk: str
    id: str

    def __init__(self,
                name: str,
                birthday: str,
                registration: str,
                workstarted: str,
                lmk: str,
                id: str) -> None:
        self.name = name
        self.birthday = birthday
        self.registration = registration
        self.workstarted = workstarted
        self.lmk = lmk
        self.id = id

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "birthday": self.birthday,
            "registration": self.registration,
            "workstarted": self.workstarted,
            "lmk": self.lmk,
            "id": self.id
        }

    def get_experience(self) -> str:
        try:
            workstarted_date = datetime.strptime(self.workstarted, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        experience_date = datetime.now() - workstarted_date

        years = experience_date.days // 365
        days = experience_date.days - (years*365)

        month = days // 30
        days = days - (month*30)

        if years == 1:
            years_postfix = "год"
        elif years == 2 or years == 3 or years == 4:
            years_postfix = "года"
        else:
            years_postfix = "лет"

        if month == 1:
            month_postfix = "месяц"
        elif month == 2 or month == 3 or month == 4:
            month_postfix = "месяца"
        else:
            month_postfix = "месяцев"

        if days == 1 or list(str(days))[-1] == 1:
            days_postfix = "день"
        elif days == 2 or days == 3 or days == 4 or list(str(days))[-1] == 2 or list(str(days))[-1] == 3 or list(str(days))[-1] == 4:
            days_postfix = "дня"
        else:
            days_postfix = "дней"

        return f"{years} {years_postfix} {month} {month_postfix} {days} {days_postfix}"
    
    def get_days_to(self):
        try:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        return self._calculate_dates(birthday, now)
        
    def _calculate_dates(self, original_date, now):
        delta1 = datetime(now.year, original_date.month, original_date.day)
        delta2 = datetime(now.year+1, original_date.month, original_date.day)
        
        return ((delta1 if delta1 > now else delta2) - now).days
    
    def get_years_old(self):
        try:
            birthday = datetime.strptime(self.birthday, '%d.%m.%Y')
        except ValueError:
            return "Неизвестно"
        
        now = datetime.now()
        delta = now - birthday
        return delta.days // 365


class EmployeeBuilder():
    def __init__(self,
                name: str = "",
                birthday: str = "",
                registration: str = "",
                workstarted: str = "",
                lmk: str = "",
                id: str = "") -> None:
        self.employee = Employee(name,
                birthday,
                registration,
                workstarted,
                lmk,
                id)
    
    def get_employee(self):
        return self.employee
    
    def __dict__(self):
        return self.employee.__dict__()