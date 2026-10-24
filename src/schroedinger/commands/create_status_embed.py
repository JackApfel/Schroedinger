import json
import logging
from pathlib import Path

import discord
from discord.ext import commands, tasks

from ..config import Config
from .status import fetch_status_embeds

logger = logging.getLogger(__name__)

base_path = Path(__file__).resolve().parent.parent.parent.parent
status_file = base_path / "data" / "status_message.json"


status_message: discord.WebhookMessage | discord.Message | None = None
status_messages: dict[int, discord.Message] = {}


def save_status_message(
    guild_id: int,
    message: discord.WebhookMessage,
) -> None:
    status_file.parent.mkdir(exist_ok=True)

    data = {"guilds": {}}

    if status_file.exists():
        with status_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

    data["guilds"][str(guild_id)] = {
        "channel_id": message.channel.id,
        "message_id": message.id,
    }

    with status_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_status_ids() -> dict[int, tuple[int, int]]:
    if not status_file.exists():
        return {}

    with status_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    guilds = data.get("guilds", {})

    return {
        int(guild_id): (
            values["channel_id"],
            values["message_id"],
        )
        for guild_id, values in guilds.items()
    }


async def restore_status_messages(
    client: commands.Bot,
) -> None:
    status_messages.clear()

    saved_ids = load_status_ids()

    for guild_id, (channel_id, message_id) in saved_ids.items():
        channel = client.get_partial_messageable(channel_id)

        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            logger.warning(
                "Status-Nachricht %s für Guild %s existiert nicht mehr.",
                message_id,
                guild_id,
            )
            continue

        if client.user is None:
            return

        if message.author.id != client.user.id:
            logger.warning(
                "Status-Nachricht %s gehört nicht zum aktuellen Bot.",
                message_id,
            )
            continue

        status_messages[guild_id] = message


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

        await interaction.response.defer()

        guild_id = interaction.guild_id

        if guild_id is None:
            return

        global status_message

        embeds = await fetch_status_embeds(config)

        message = await interaction.followup.send(
            embeds=embeds,
            wait=True,
        )

        status_messages[guild_id] = message
        save_status_message(guild_id, message)


@tasks.loop(seconds=10)
async def update_embeds(config: Config) -> None:
    if not status_messages:
        return

    embeds = await fetch_status_embeds(config)

    for guild_id, message in list(status_messages.items()):
        try:
            await message.edit(embeds=embeds)
        except discord.errors.NotFound as error:
            logger.error("Message not found! %s", error)
