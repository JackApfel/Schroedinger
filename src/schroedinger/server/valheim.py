import logging

import a2s

from ..config import VALHEIM_HOST_IP, VALHEIM_PORT
from ..models.server_status import ValheimServerStatus

logger = logging.getLogger(__name__)


async def check_valheim_server_status() -> ValheimServerStatus:
    try:
        info = await a2s.ainfo((VALHEIM_HOST_IP, VALHEIM_PORT), timeout=3.0)  # type: ignore

        logger.info(info)

        return ValheimServerStatus(
            description=info.server_name,
            online=True,
            players=info.player_count,
            max_players=info.max_players,
            latency=info.ping * 1000,
            version=info.version,
            protocol=info.protocol,
            map_name=info.map_name,
            folder=info.folder,
            game=info.game,
            app_id=info.app_id,
            bot_count=info.bot_count,
            server_type=info.server_type,
            platform=info.platform,
            password_protected=info.password_protected,
            vac_enabled=info.vac_enabled,
            edf=info.edf,
            port=info.port,
            steam_id=info.steam_id,
            stv_port=info.stv_port,
            stv_name=info.stv_name,
            keywords=info.keywords,
            game_id=info.game_id,
        )

    except Exception as e:
        logger.error("Valheim Status Error: %s", repr(e))
        return ValheimServerStatus(
            description="Unknown",
            online=False,
            players=None,
            max_players=None,
            latency=None,
            version="Unknown",
            protocol=0,
            map_name="Unknown",
            folder="Unknown",
            game="Unknown",
            app_id=0,
            bot_count=None,
            server_type="Unknown",
            platform="Unknown",
            password_protected=None,
            vac_enabled=None,
            edf=0,
            port=None,
            steam_id=None,
            stv_port=None,
            stv_name=None,
            keywords=None,
            game_id=None,
        )
