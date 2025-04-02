import hashlib

from app.core.types.employee import Employee, EmployeeBuilder
from app.core.types.user import User, UserBuilder
from app.core.types.app import App, AppBuilder

__all__ = [
    'Employee',
    'EmployeeBuilder',
    'User',
    'UserBuilder',
    'App',
    'AppBuilder'
]

class CallbackData:
    prefix = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __init_subclass__(cls, prefix=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if prefix is not None:
            cls.prefix = prefix

    def pack(self):
        parts = [self.prefix] if self.prefix else []
        parts.extend(str(value) for value in self.__dict__.values() if value is not self.prefix)
        return ':'.join(parts)
    
    def hash(self):
        data = self.pack()
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()

    @classmethod
    def unpack(cls, callback_string):
        parts = callback_string.split(':')
        if cls.prefix and parts[0] != cls.prefix:
            raise ValueError("Invalid prefix")
        kwargs = dict(zip(cls.__init__.__code__.co_varnames[1:], parts[1:] if cls.prefix else parts))
        return cls(**kwargs)