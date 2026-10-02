import logging

import a2s

from ..config import VALHEIM_HOST_IP, VALHEIM_PORT
from ..models.server_status import ServerStatus

logger = logging.getLogger(__name__)


async def check_valheim_server_status() -> ServerStatus:
    try:
        info = await a2s.ainfo((VALHEIM_HOST_IP, VALHEIM_PORT), timeout=3.0)  # type: ignore
        return ServerStatus(
            description=info.server_name,
            online=True,
            players=info.player_count,
            max_players=info.max_players,
            latency=info.ping * 1000,
            version=info.version,
        )

    except Exception as e:
        logger.error("Valheim Status Error: %s", repr(e))
        return ServerStatus(
            description="Unknown",
            online=False,
            players=0,
            max_players=0,
            latency=0,
            version="Unknown",
        )
