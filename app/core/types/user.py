from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class User():
    id: str
    chat_notify: bool
    registration: str
    role: Role


    def __init__(self,
                id: str,
                chat_notify: bool,
                registration: str,
                role: Role
    ) -> None:
        self.id = id
        self.chat_notify = chat_notify
        self.registration = registration
        self.role = role

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "chat_notify": self.chat_notify,
            "registration": self.registration,
            "role": self.role.value
        }


class UserBuilder():
    def __init__(self,
                id: str = "",
                chat_notify: str = "",
                registration: str = "",
                role: str = ""
                
    ) -> None:
        self.user = User(
            id,
            chat_notify,
            registration,
            role
        )
    
    def get_user(self):
        return self.user
    
    def __dict__(self):
        return self.user.__dict__()