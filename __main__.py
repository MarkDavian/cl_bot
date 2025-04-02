"""
Главный модуль приложения CL Bot.

Этот файл является точкой входа для запуска бота учета персонала для кофеен.
Он запускает три основных процесса:
1. Основной бот Telegram для взаимодействия с пользователями
2. Систему уведомлений для отслеживания важных событий
3. Сервис резервного копирования для автоматического создания бэкапов

Каждый процесс запускается в отдельном потоке для обеспечения независимой работы
компонентов и предотвращения блокировки основного интерфейса бота.
"""

import asyncio
import multiprocessing

from app.telegram import start_bot
from app.notifier import start_notifier
from app.backup import start_backup


async def main():
    """
    Асинхронная функция для запуска Telegram-бота.
    Выполняет инициализацию и запуск основного цикла бота.
    """
    await start_bot()


def run_bot():
    """
    Функция для запуска бесконечного цикла обработки событий бота.
    Создает задачу для выполнения основной функции бота и запускает
    цикл событий для обработки всех асинхронных операций.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


if __name__ == '__main__':
    print('STARTING...')
    # Создание отдельных процессов для каждого компонента системы
    main_proc = multiprocessing.Process(target=run_bot)
    notifier_proc = multiprocessing.Process(target=start_notifier)
    backup_proc = multiprocessing.Process(target=start_backup)

    # Запуск всех процессов
    main_proc.start()
    notifier_proc.start()
    backup_proc.start()