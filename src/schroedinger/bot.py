import asyncio
import logging

import discord
from discord.ext import commands

from schroedinger.commands.status import register_status_command
from schroedinger.config import load_config

from .logger import logger


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
    logger = logging.getLogger(__name__)

    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(
        intents=intents,
        command_prefix="/",
    )

    logger.info("Bot.py main called")

    config = load_config()

    register_status_command(config=config, client=client)

    @client.event
    async def on_ready():
        logger.info("We have logged in as %s", client.user)
        await client.tree.sync()
        logger.info("Slash-Commands erfolgreich synchronisiert!")

    client.run(config.token, log_handler=None)
