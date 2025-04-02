from .subjects.export import reg_export_callback
from .subjects.query.query_menu import reg_query_main_callback
from .subjects.espresso_machine_health import reg_espresso_health_main_callback


def reg_callback_menu(dp):
    reg_export_callback(dp)
    reg_query_main_callback(dp)
    reg_espresso_health_main_callback(dp)