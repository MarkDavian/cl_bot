"""
Модуль-заглушка для работы с autodoc Sphinx.

Этот модуль содержит заглушки для импортов, которые могут вызвать проблемы 
при сборке документации из-за отсутствия файлов или зависимостей.
"""

class Mock:
    """Класс-заглушка для импортов в документации."""
    
    def __init__(self, *args, **kwargs):
        pass
        
    def __call__(self, *args, **kwargs):
        return Mock()
        
    @classmethod
    def __getattr__(cls, name):
        return Mock()
        
    def __getitem__(self, name):
        return Mock()
        
    def __bool__(self):
        return False


# Список модулей, которые нужно замокать
MOCK_MODULES = [
    'aiogram', 'aiogram.dispatcher', 'aiogram.dispatcher.filters', 
    'aiogram.contrib.fsm_storage.memory', 'aiogram.dispatcher.filters.state',
    'pandas', 'openpyxl', 'openpyxl.styles', 'openpyxl.utils'
]

# Создание заглушек для модулей
import sys
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

# Заглушка для app модулей
sys.modules['app'] = Mock()
sys.modules['app.core'] = Mock()
sys.modules['app.core.types'] = Mock()
sys.modules['app.core.types.app'] = Mock()
sys.modules['app.core.types.employee'] = Mock()
sys.modules['app.core.types.types'] = Mock()
sys.modules['app.core.db'] = Mock()
sys.modules['app.core.db.database'] = Mock()
sys.modules['app.backup'] = Mock()
sys.modules['app.backup.__init__'] = Mock()
sys.modules['app.notifier'] = Mock()

# Заглушка для модуля states
class StatesGroup:
    def __init__(self, *args, **kwargs):
        pass
    
class State:
    def __init__(self, *args, **kwargs):
        pass

# Замокаем модуль app.telegram.handlers.states
class states_mock:
    class AddEmployee(StatesGroup):
        """Состояния для добавления сотрудника."""
        waiting_for_name = State()
        waiting_for_birth = State()
        waiting_for_registration = State()
        waiting_for_workstarted = State()
        waiting_for_lmk = State()
        
    class DelEmployee(StatesGroup):
        """Состояния для удаления сотрудника."""
        waiting_for_confirmation = State()

# Заглушка для команд Telegram
class commands_common_mock:
    """Заглушка для модуля команд Telegram."""
    
    async def cmd_start(message):
        """Обработчик команды /start."""
        pass
        
    async def cmd_help(message):
        """Обработчик команды /help."""
        pass
        
    async def cmd_backup(message):
        """Обработчик команды /backup."""
        pass

# Заглушка для модуля меню
class menu_common_mock:
    """Заглушка для модуля меню Telegram."""
    
    class MenuCallback:
        """Класс для обработки callback-запросов от кнопок меню."""
        pass

# Заглушка для модуля commands.menu
class commands_menu_mock:
    """Модуль команд меню Telegram."""
    
    async def show_main_menu(message):
        """Отображает главное меню бота."""
        pass

# Заглушка для модуля commands.emps
class commands_emps_mock:
    """Модуль управления сотрудниками."""
    
    async def add_employee(message):
        """Запуск процесса добавления сотрудника."""
        pass
        
    async def list_employees(message):
        """Отображение списка сотрудников."""
        pass
        
    async def delete_employee(message):
        """Запуск процесса удаления сотрудника."""
        pass

# Заглушка для модуля commands.emps_ext
class commands_emps_ext_mock:
    """Модуль расширенного управления сотрудниками."""
    
    async def edit_employee(message):
        """Редактирование данных сотрудника."""
        pass

# Заглушка для модуля commands.settings
class commands_settings_mock:
    """Модуль управления настройками бота."""
    
    async def show_settings(message):
        """Отображение настроек бота."""
        pass

# Заглушка для модуля commands.settings.time_intervals
class commands_settings_time_intervals_mock:
    """Модуль настройки временных интервалов уведомлений."""
    
    async def set_dr_interval(message):
        """Установка интервала для проверки дней рождения."""
        pass
        
    async def set_lmk_interval(message):
        """Установка интервала для проверки медицинских книжек."""
        pass

# Заглушки для классов типов данных
class Employee:
    """Класс сотрудника."""
    def __init__(self, name=None, birthday=None, registration=None, 
                 workstarted=None, lmk=None, id=None, cert_base=None):
        self.name = name
        self.birthday = birthday
        self.registration = registration
        self.workstarted = workstarted
        self.lmk = lmk
        self.id = id
        self.cert_base = cert_base

class TestResult:
    """Класс результата теста."""
    def __init__(self, completion_time=None, score=None, rank=None, date=None, type=None):
        self.completion_time = completion_time
        self.score = score
        self.rank = rank
        self.date = date
        self.type = type

class EmployeeBuilder:
    """Класс строителя объектов сотрудника."""
    def __init__(self, name=None, birthday=None, registration=None, 
                 workstarted=None, lmk=None, id=None, cert_base=None):
        self.employee = Employee(name, birthday, registration, workstarted, lmk, id, cert_base)
    
    def __dict__(self):
        """Преобразование в словарь."""
        return vars(self.employee)

class App:
    """Класс настроек приложения."""
    def __init__(self, password=None, lmk_notify_time_interval=None, 
                 dr_notify_time_interval=None, anniversary_time_interval=None, 
                 certs_time_interval=None, time_to_notify=None):
        self.password = password
        self.lmk_notify_time_interval = lmk_notify_time_interval
        self.dr_notify_time_interval = dr_notify_time_interval
        self.anniversary_time_interval = anniversary_time_interval
        self.certs_time_interval = certs_time_interval
        self.time_to_notify = time_to_notify

class AppBuilder:
    """Класс строителя объектов настроек приложения."""
    def __init__(self, password=None, lmk_notify_time_interval=None, 
                 dr_notify_time_interval=None, anniversary_time_interval=None, 
                 certs_time_interval=None, time_to_notify=None):
        self.app = App(password, lmk_notify_time_interval, dr_notify_time_interval,
                       anniversary_time_interval, certs_time_interval, time_to_notify)
    
    def __dict__(self):
        """Преобразование в словарь."""
        return vars(self.app)

class Interval:
    """Класс интервала времени."""
    def __init__(self, type=None, button_txt=None):
        self.type = type
        self.button_txt = button_txt

# Экспорт классов типов данных
sys.modules['app.core.types.types'].Employee = Employee
sys.modules['app.core.types.types'].EmployeeBuilder = EmployeeBuilder
sys.modules['app.core.types.employee'].Employee = Employee
sys.modules['app.core.types.employee'].TestResult = TestResult
sys.modules['app.core.types.app'].App = App
sys.modules['app.core.types.app'].AppBuilder = AppBuilder
sys.modules['app.core.types.app'].Interval = Interval
sys.modules['app.core.types.app'].NAMED_INTERVALS = {
    "1 день": Interval(86400, "1 день"),
    "2 дня": Interval(172800, "2 дня"),
    "3 дня": Interval(259200, "3 дня"),
    "7 дней": Interval(604800, "7 дней"),
    "14 дней": Interval(1209600, "14 дней"),
    "30 дней": Interval(2592000, "30 дней")
}

# Регистрируем заглушки модулей Telegram
sys.modules['app.telegram'] = Mock()
sys.modules['app.telegram.handlers'] = Mock()
sys.modules['app.telegram.handlers.states'] = states_mock
sys.modules['app.telegram.handlers.commands'] = Mock()
sys.modules['app.telegram.handlers.commands.common'] = commands_common_mock
sys.modules['app.telegram.handlers.commands.menu'] = commands_menu_mock
sys.modules['app.telegram.handlers.commands.menu.common'] = menu_common_mock
sys.modules['app.telegram.handlers.commands.emps'] = commands_emps_mock
sys.modules['app.telegram.handlers.commands.emps_ext'] = commands_emps_ext_mock
sys.modules['app.telegram.handlers.commands.settings'] = commands_settings_mock
sys.modules['app.telegram.handlers.commands.settings.time_intervals'] = commands_settings_time_intervals_mock

# Заглушки для config
class SETTINGS:
    BOT_TOKEN = "fake_token"
    CHAT_ID = "fake_chat_id"
    INTERVAL_24 = 86400
    LMK_NOTIFY_TIME_INTERVAL = 86400
    DR_NOTIFY_TIME_INTERVAL = 86400
    ANNIVERSARY_TIME_INTERVAL = 86400
    CERTS_TIME_INTERVAL = 86400
    TIME_TO_NOTIFY = "12:00"

# Необходимая для модуля app.core.types.app переменная 
STANDART_APP_SETTINGS = {
    "PASSWORD": "password",
    "LMK_NOTIFY_TIME_INTERVAL": 86400,
    "DR_NOTIFY_TIME_INTERVAL": 86400,
    "ANNIVERSARY_TIME_INTERVAL": 86400,
    "CERTS_TIME_INTERVAL": 86400,
    "TIME_TO_NOTIFY": "12:00"
}

# Заглушки для других важных классов и функций
ALLOWED_INTERVALS = {
    "1 день": 86400,
    "2 дня": 172800,
    "3 дня": 259200,
    "7 дней": 604800,
    "14 дней": 1209600,
    "30 дней": 2592000
}
