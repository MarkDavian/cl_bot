from app.core.types import CallbackData


class EspressoCallbackData(CallbackData, prefix='espresso'):
    def __init__(self, action="", page=1, key=""):
        super().__init__(
            action=action, 
            page=page,
            key=key
        )
