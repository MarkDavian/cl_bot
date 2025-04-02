from app.core.types import User
from app.core.funcs.app import get_app
from app.core.funcs.correct_date import humanize_date


def __get_info_bool(info: bool) -> str:
    if info == True:
        return 'Включено'
    return 'Отключено'


def __main_settings_msg(user: User) -> str:
    app = get_app()
    return (
            "<b>НАСТРОЙКИ</b>\n"
            f"<b>Уведомления мне в чат:</b> {__get_info_bool(user.chat_notify)}\n\n"
            "<b>Интервалы уведомлений:</b>\n"
            f"ДР: {humanize_date(app.dr_notify_time_interval)}\n"
            f"ЛМК: {humanize_date(app.lmk_notify_time_interval)}\n"
            f"ЮБИЛЕЙ: {humanize_date(app.anniversary_time_interval)}\n"
            f"СЕРТИФИКАТЫ: {humanize_date(app.certs_time_interval)}\n\n"
            f"<b>Время оповещения:</b> {app.time_to_notify}\n"
            f"<b>Пароль бота:</b> {app.password}\n"
        )