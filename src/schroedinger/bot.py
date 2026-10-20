import logging

import discord
from discord.ext import commands

from schroedinger.commands.create_status_embed import (
    register_create_status_embed_command,
    restore_status_messages,
    update_embeds,
)
from schroedinger.commands.status import register_status_command
from schroedinger.config import load_config

from .logger import logger

logger = logging.getLogger(__name__)


def main() -> None:

    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(
        intents=intents,
        command_prefix="/",
    )

    logger.info("Bot.py main called")

    config = load_config()

    register_status_command(config=config, client=client)
    register_create_status_embed_command(config=config, client=client)

    @client.event
    async def on_ready():
        logger.info("We have logged in as %s", client.user)

        await client.tree.sync()

        await restore_status_messages(client=client)
        if not update_embeds.is_running():
            update_embeds.start(config)

        logger.info("Slash-Commands erfolgreich synchronisiert!")

    client.run(config.token, log_handler=None)
