from app.core.types.types import App, AppBuilder
from app.core.db.database import AppSettings


def get_app() -> App:
    with AppSettings() as s:
        info = s.get()
    
    return AppBuilder(**info).get_app()


def get_password() -> str:
    with AppSettings() as s:
        return s.get_password()
    

def change_password(text: str) -> str:
    with AppSettings() as s:
        password = s.set_password(text)
    return password