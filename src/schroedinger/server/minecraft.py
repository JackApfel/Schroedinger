import logging

from mcstatus import JavaServer

from ..config import MINECRAFT_HOST_IP, MINECRAFT_PORT
from ..models.server_status import ServerStatus

logger = logging.getLogger(__name__)


async def check_mc_server_status() -> ServerStatus:
    server = JavaServer(MINECRAFT_HOST_IP, MINECRAFT_PORT)
    try:
        status = await server.async_status()

        return ServerStatus(
            description=status.raw.get("description"),
            online=True,
            players=status.players.online,
            max_players=status.players.max,
            latency=status.latency,
            version=status.version.name,
        )

    except Exception as e:
        logger.error("Minecraft Status Error: %s", repr(e))

        return ServerStatus(
            description="Unknown",
            online=False,
            players=0,
            max_players=0,
            latency=0,
            version="Unknown",
        )
