import asyncio

from app.telegram import start_bot


async def main():
    await start_bot()


if __name__ == '__main__':
    print('STARTING...')
    asyncio.run(main())