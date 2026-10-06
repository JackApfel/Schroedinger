import logging
import time

import aiohttp
from aiohttp import ClientTimeout

from ..config import Config
from ..models.server_status import HytaleServerStatus

logger = logging.getLogger(__name__)


async def check_hytale_server_status(config: Config) -> HytaleServerStatus:
    try:
        start_time = time.perf_counter()
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"https://{config.hytale_host_ip}:{config.hytale_port + 3}/Nitrado/Query",
                ssl=False,
                timeout=ClientTimeout(3.0),
            ) as response,
        ):
            response.raise_for_status()
            data = await response.json()

            end_time = time.perf_counter()
            latency = (end_time - start_time) * 1000
            max_players = data["Server"]["MaxPlayers"]
            version = data["Server"]["Version"]
            name = data["Server"]["Name"]
            current_players = data["Universe"]["CurrentPlayers"]
            default_world = data["Universe"]["DefaultWorld"]

            return HytaleServerStatus(
                description=name,
                online=True,
                players=current_players,
                max_players=max_players,
                latency=latency,
                version=version,
                default_world=default_world,
            )

    except Exception as error:
        logger.error("Server nicht erreichbar: %s", error)
        return HytaleServerStatus(
            description=None,
            online=False,
            players=None,
            max_players=None,
            latency=None,
            version=None,
            default_world=None,
        )
