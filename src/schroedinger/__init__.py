import asyncio
import logging

import discord
import dotenv
from discord.ext import commands

from .config import (
    TOKEN,
)

logger = logging.getLogger(__name__)
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix="/")


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    logger.info("[%r exited with %s]", cmd, proc.returncode)
    if stdout:
        logger.info("[stdout] %s", stdout.decode())
    if stderr:
        logger.error("[stderr] %s", stderr.decode())
    return proc.returncode


def main() -> None:
    # Enviromenrt variablen holen

    @client.event
    async def on_ready():
        logger.info("We have logged in as %s", client.user)
        await client.tree.sync()
        logger.info("Slash-Commands erfolgreich synchronisiert!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

    if TOKEN != None:
        client.run(TOKEN, log_handler=None)

        return
