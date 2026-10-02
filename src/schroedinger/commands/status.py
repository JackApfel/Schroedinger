from typing import Literal
import a2s
import discord
import logging
from mcstatus import JavaServer
from ..config import MINECRAFT_HOST_IP, MINECRAFT_PORT, VALHEIM_HOST_IP, VALHEIM_PORT

logger = logging.getLogger(__name__)


async def check_valheim_server_status() -> discord.Embed:
    try:
        info = await a2s.ainfo((VALHEIM_HOST_IP, VALHEIM_PORT), timeout=3.0)  # type: ignore

        embed = discord.Embed(
            title="⚔️ Valheim Server Status",
            description=f"**{info.server_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="👥 Spieler", value=f"{info.player_count} / {info.max_players}", inline=True)
        embed.add_field(name="🗺️ Welt", value=f"{info.map_name}", inline=True)
        embed.add_field(name="🧩 Version", value=f"{info.version}", inline=True)
        embed.add_field(name="📡 Ping", value=f"{info.ping * 1000:.0f} ms", inline=True)
        embed.add_field(name="🔒 Passwortschutz", value="Ja" if info.password_protected else "Nein", inline=True)

    except Exception as e:
        logger.error("Valheim Status Error: %s", repr(e))

        embed = discord.Embed(
            title="⚔️ Valheim Server Status",
            description="Server nicht erreichbar",
            color=discord.Color.red()
        )
    return embed



async def check_mc_server_status() -> discord.Embed:
    server = JavaServer(MINECRAFT_HOST_IP, MINECRAFT_PORT)
    try:
        status = await server.async_status()

        modpack = status.raw.get("betterStatus", {})
        modpack_name = modpack.get("name", status.motd.raw)
        modpack_version = modpack.get("version")
        modpack_text = f"{modpack_name} (v{modpack_version})" if modpack_version else modpack_name

        embed = discord.Embed(
            title="⛏️ Minecraft Server Status",
            description=f"{status.description}",
            color=discord.Color.green()
        )

        embed.add_field(name="👥 Spieler", value=f"{status.players.online} / {status.players.max}", inline=True)
        embed.add_field(name="⚙️ Modpack", value=modpack_text, inline=True)
        embed.add_field(name="🧱 Minecraft", value=f"{status.version.name}", inline=True)
        embed.add_field(name="📡 Latenz", value=f"{status.latency:.0f} ms", inline=True)

    except Exception as e:
        logger.error("Minecraft Status Error: %s", repr(e))
        embed = discord.Embed(
            title="⛏️ Minecraft Server Status",
            description=f"Server nicht ereichbar",
            color=discord.Color.red()
        )

    return embed


def register_status_command(client) -> None:
    @client.tree.command(name="status", description="Check server status")
    async def status(interaction: discord.Interaction, game: Literal["all","Minecraft", "Valheim"]):
        await interaction.response.defer()
        embeds = []

        if game == "Minecraft" or game == "all":
            embeds.append(await  check_mc_server_status())
            logger.info("Minecraft status command executed")

            if game == "all":
                logger.info("Minecraft embed added to embeds list and moving to Valheim status check")


        if game == "Valheim" or game == "all":
            logger.info("Checking Valheim server status...")
            embeds.append(await check_valheim_server_status())
            logger.info("Valheim status command executed")

            if game == "all":
                logger.info("Valheim status command executed after Minecraft status check")


        logger.info("Anzahl Embeds: %s", len(embeds))
        logger.info("Embed-Titel: %s", [embed.title for embed in embeds])

        try:
            await interaction.followup.send(embeds=embeds)
        except Exception as error:
            logger.error(f"Fehler beim Senden der Embeds: {error!r}")
        logger.info("status command executed")