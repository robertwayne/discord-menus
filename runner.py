# This is a testing module which interfaces with the documentation examples. You will need to
# have an environment variable called 'DPYMENUS_BOT_TOKEN' set in order for this to run. This
# module must live in the root directory.
#
# You can run this file directly or with `poetry run examples`.

import asyncio
import logging
import os
import sys

from cogwatch import watch
from discord.ext import commands
from dotenv import load_dotenv

try:
    import uvloop
except ImportError:
    uvloop = None

logging.basicConfig(level=logging.INFO)

if sys.platform in {'linux', 'macos'}:
    uvloop.install()
    logging.info('Using `uvloop` asyncio event loop.')

load_dotenv()


class ExampleRunner(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.')

    @watch(path='examples', debug=False, preload=True)
    async def on_ready(self):
        logging.info('Bot ready.')

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)


async def main():
    client = ExampleRunner()
    await client.start(os.getenv('DPYMENUS_BOT_TOKEN'))


def __poetry_run():
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())
