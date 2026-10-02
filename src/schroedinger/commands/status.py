import asyncio
import logging
from typing import Literal

import discord

from ..server.minecraft import check_mc_server_status
from ..server.valheim import check_valheim_server_status

logger = logging.getLogger(__name__)


def create_server_embed(server_status, title: str) -> discord.Embed:
    online = server_status.online
    embed = discord.Embed(
        title=title,
        description=f"**{server_status.description}**",
        color=discord.Color.green() if online else discord.Color.red(),
    )
    embed.add_field(
        name="🟢 Status",
        value="Online" if online else "Offline",
        inline=True,
    )
    embed.add_field(
        name="👥 Spieler",
        value=f"{server_status.players} / {server_status.max_players}",
        inline=True,
    )
    embed.add_field(
        name="📡 Ping",
        value=f"{server_status.latency:.0f} ms",
        inline=True,
    )
    embed.add_field(
        name="🧩 Version",
        value=f"{server_status.version}",
        inline=True,
    )
    return embed


def register_status_command(client) -> None:
    @client.tree.command(name="status", description="Check server status")
    async def status(
        interaction: discord.Interaction, game: Literal["all", "Minecraft", "Valheim"]
    ):
        await interaction.response.defer()
        embeds = []

        if game == "all":
            valheim_status, minecraft_status = await asyncio.gather(
                check_valheim_server_status(), check_mc_server_status()
            )
            embeds.extend(
                [
                    create_server_embed(minecraft_status, "⛏️ Minecraft Server Status"),
                    create_server_embed(valheim_status, "⚔️ Valheim Server Status"),
                ]
            )

        if game == "Minecraft":
            mc_server_status = await check_mc_server_status()

            logger.info("Minecraft status command executed")
            embeds.append(
                create_server_embed(mc_server_status, "⛏️ Minecraft Server Status")
            )

        if game == "Valheim":
            logger.info("Checking Valheim server status...")
            vh_server_status = await check_valheim_server_status()
            embeds.append(
                create_server_embed(vh_server_status, "⚔️ Valheim Server Status")
            )
            logger.info("Valheim status command executed")

        logger.info("Anzahl Embeds: %s", len(embeds))
        logger.info("Embed-Titel: %s", [embed.title for embed in embeds])

        try:
            await interaction.followup.send(embeds=embeds)
        except Exception as error:
            logger.error("Fehler beim Senden der Embeds: %r", error)
        logger.info("status command executed")
