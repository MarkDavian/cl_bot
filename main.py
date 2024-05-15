import asyncio
import multiprocessing

from app.telegram import start_bot
from app.notifier import start_notifier


async def main():
    await start_bot()


def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


if __name__ == '__main__':
    print('STARTING...')
    main_proc = multiprocessing.Process(target=run_bot)
    notifier_proc = multiprocessing.Process(target=start_notifier)

    main_proc.start()
    notifier_proc.start()

    # run_bot()