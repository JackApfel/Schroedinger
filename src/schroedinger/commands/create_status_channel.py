import logging
from pathlib import Path

import discord
from discord.ext import commands, tasks

from ..config import Config
from .status import fetch_status_embeds

logger = logging.getLogger(__name__)

base_path = Path(__file__).resolve().parent.parent.parent


status_message: discord.WebhookMessage | None = None


def register_create_status_embed_command(
    config: Config,
    client: commands.Bot,
) -> None:
    @client.tree.command(
        name="create_status_embed",
        description="Creates and updates an embed with current server states",
    )
    async def create_status_embed(
        interaction: discord.Interaction,
    ) -> None:

        global status_message

        await interaction.response.defer()

        embeds = await fetch_status_embeds(config)

        status_message = await interaction.followup.send(embeds=embeds, wait=True)

        logger.info("status message: %s", status_message)


@tasks.loop(seconds=10)
async def update_embeds(config: Config) -> None:
    if status_message is None:
        return

    embeds = await fetch_status_embeds(config)
    await status_message.edit(embeds=embeds)
