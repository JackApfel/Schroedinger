import asyncio
import logging
from typing import Literal

import discord

from ..models.server_status import (
    HytaleServerStatus,
    MinecraftServerStatus,
    ServerStatus,
    ValheimServerStatus,
)
from ..server.hytale import check_hytale_server_status
from ..server.minecraft import check_mc_server_status
from ..server.valheim import check_valheim_server_status

logger = logging.getLogger(__name__)


def format_bool(value: bool | None, true_label: str, false_label: str) -> str:
    if value is None:
        return "Unbekannt"
    return true_label if value else false_label


def create_server_embed(server_status: ServerStatus, title: str) -> discord.Embed:
    online = server_status.online
    embed = discord.Embed(
        title=title,
        description=f"**{server_status.description}**"
        if server_status.description
        else "Unknown",
        color=(
            discord.Color.green()
            if online is True
            else discord.Color.red()
            if online is False
            else discord.Color.greyple()
        ),
    )
    embed.add_field(
        name="🟢 Status",
        value=format_bool(online, "Online", "Offline"),
        inline=True,
    )
    embed.add_field(
        name="👥 Spieler",
        value=(
            f"{server_status.players} / {server_status.max_players}"
            if server_status.players is not None
            and server_status.max_players is not None
            else "Unbekannt"
        ),
        inline=True,
    )
    embed.add_field(
        name="📡 Ping",
        value=(
            f"{server_status.latency:.0f} ms"
            if server_status.latency is not None
            else "Unbekannt"
        ),
        inline=True,
    )
    embed.add_field(
        name="🏷️ Version",
        value=server_status.version or "Unbekannt",
        inline=True,
    )

    return embed


def create_minecraft_server_embed(
    server_status: MinecraftServerStatus, title: str
) -> discord.Embed:

    embed = create_server_embed(server_status, title)

    embed.add_field(
        name="🧱 Modded",
        value=format_bool(server_status.is_modded, "Ja", "Nein"),
        inline=True,
    )
    embed.add_field(
        name="🔐 Secure Chat",
        value=format_bool(server_status.enforces_secure_chat, "Aktiv", "Inaktiv"),
        inline=True,
    )
    if server_status.is_modded and server_status.modpack:
        embed.add_field(
            name="📦 Modpack",
            value=f"{server_status.modpack.name}",
            inline=True,
        )
        embed.add_field(
            name="🏷️ Modpack-Version",
            value=f"{server_status.modpack.version}",
            inline=True,
        )
    return embed


def create_valheim_server_embed(
    server_status: ValheimServerStatus, title: str
) -> discord.Embed:

    embed = create_server_embed(server_status, title)

    embed.add_field(
        name="🗺️ Welt",
        value=server_status.map_name or "Unbekannt",
        inline=True,
    )
    embed.add_field(
        name="🔒 Passwort",
        value=format_bool(
            server_status.password_protected,
            "Erforderlich",
            "Nicht erforderlich",
        ),
        inline=True,
    )
    embed.add_field(
        name="🛡️ VAC",
        value=format_bool(server_status.vac_enabled, "Aktiv", "Inaktiv"),
        inline=True,
    )
    # embed.add_field(
    #     name="🔌 Port",
    #     value=str(server_status.port)
    #     if server_status.port is not None
    #     else "Unbekannt",
    #     inline=True,
    # )

    return embed


def create_hytale_server_embed(
    server_status: HytaleServerStatus, title: str
) -> discord.Embed:
    embed = create_server_embed(server_status, title)

    # embed.add_field(
    #     name="🗺️ Welt",
    #     value=server_status.default_world or "Unbekannt",
    #     inline=True,
    # )

    return embed


def register_status_command(client) -> None:
    @client.tree.command(name="status", description="Check server status")
    async def status(
        interaction: discord.Interaction,
        game: Literal["all", "Minecraft", "Valheim", "Hytale"],
    ):
        await interaction.response.defer()
        embeds = []

        if game == "all":
            valheim_status, minecraft_status, hytale_status = await asyncio.gather(
                check_valheim_server_status(),
                check_mc_server_status(),
                check_hytale_server_status(),
            )
            embeds.extend(
                [
                    create_minecraft_server_embed(
                        minecraft_status, "⛏️ Minecraft Server Status"
                    ),
                    create_valheim_server_embed(
                        valheim_status, "⚔️ Valheim Server Status"
                    ),
                    create_hytale_server_embed(hytale_status, "🗡️ Hytale Server Status"),
                ]
            )

        if game == "Minecraft":
            mc_server_status = await check_mc_server_status()
            logger.info("Minecraft status command executed")
            embeds.append(
                create_minecraft_server_embed(
                    mc_server_status, "⛏️ Minecraft Server Status"
                )
            )

        if game == "Valheim":
            logger.info("Checking Valheim server status...")
            vh_server_status = await check_valheim_server_status()
            embeds.append(
                create_valheim_server_embed(vh_server_status, "⚔️ Valheim Server Status")
            )
            logger.info("Valheim status command executed")

        if game == "Hytale":
            logger.info("Checking Hytale server status...")
            ht_server_status = await check_hytale_server_status()
            embeds.append(
                create_hytale_server_embed(ht_server_status, "🗡️ Hytale Server Status")
            )

        logger.info("Anzahl Embeds: %s", len(embeds))
        logger.info("Embed-Titel: %s", [embed.title for embed in embeds])

        try:
            await interaction.followup.send(embeds=embeds)
        except Exception as error:
            logger.error("Fehler beim Senden der Embeds: %r", error)
        logger.info("status command executed")
