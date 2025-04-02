from dataclasses import dataclass

from app.core.types import CallbackData


class MenuCallbackData(CallbackData, prefix='menu'):
    action: str


@dataclass
class MenuButton:
    text: str
    callback_data: MenuCallbackData