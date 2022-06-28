import asyncio
import os

from jgram import Registry
from jgram.context import Context
from jgram.manager import WindowsManager


async def name_formatter(update, manager: WindowsManager, context: Context):
    context.data['name'] = update.text # saved in storage


async def age_formatter(update, manager: WindowsManager, context: Context):
    context.data['age'] = update.text


async def main():
    registry = Registry(token=os.getenv('BOT_TOKEN'))
    registry.manager.load_windows('simple_windows.json')
    registry.register_middleware(name_formatter, name='write_age')
    registry.register_middleware(age_formatter, name='save_data')

    try:
        await registry.start()
    finally:
        await registry.close()


if __name__ == '__main__':
    asyncio.run(main())

