from app.core.types import CallbackData


class EmpCallbackData(CallbackData, prefix='staff'):
    action: str
    emp_id: str

    def __init__(self, action: str, emp_id: str):
        self.action = action
        self.emp_id = emp_id
        super().__init__()


class CLTestsCallbackData(CallbackData, prefix='test'):
    action: str
    test_id: str
    page: int

    def __init__(self, action: str, test_id: str, page: int):
        self.action = action
        self.test_id = test_id
        self.page = page
        super().__init__()