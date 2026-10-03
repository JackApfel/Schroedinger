import logging

from mcstatus import JavaServer

from ..config import MINECRAFT_HOST_IP, MINECRAFT_PORT
from ..models.server_status import MinecraftModpack, MinecraftServerStatus

logger = logging.getLogger(__name__)


async def check_mc_server_status() -> MinecraftServerStatus:
    server = JavaServer(MINECRAFT_HOST_IP, MINECRAFT_PORT)  # type: ignore
    try:
        status = await server.async_status()

        better_status = status.raw.get("betterStatus")
        modpack = (
            MinecraftModpack(
                name=better_status["name"],
                version=better_status["version"],
            )
            if better_status
            else None
        )
        return MinecraftServerStatus(
            description=status.description,
            online=True,
            players=status.players.online,
            max_players=status.players.max,
            latency=status.latency,
            version=status.version.name,
            is_modded=status.raw.get("isModded", False),
            modpack=modpack,
            enforces_secure_chat=status.raw.get("enforcesSecureChat"),
            prevents_chat_reports=status.raw.get("preventsChatReports"),
            protocol_version=status.version.protocol,
        )

    except Exception as e:
        logger.error("Minecraft Status Error: %s", e)

        return MinecraftServerStatus(
            description="Unknown",
            online=False,
            players=0,
            max_players=0,
            latency=0,
            version="Unknown",
            is_modded=False,
            modpack=None,
            enforces_secure_chat=False,
            prevents_chat_reports=False,
            protocol_version=0,
        )
