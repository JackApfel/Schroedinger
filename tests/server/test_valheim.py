from types import SimpleNamespace

import pytest

from schroedinger.models.server_status import ValheimServerStatus
from schroedinger.server import valheim


@pytest.mark.asyncio
async def test_check_valheim_server_status_returns_online_status(
    monkeypatch,
    config,
):
    fake_info = SimpleNamespace(
        server_name="Mein Valheim Server",
        player_count=4,
        max_players=10,
        ping=0.042,
        version="0.219.16",
        protocol=17,
        map_name="Meadows",
        folder="valheim",
        game="Valheim",
        app_id=892970,
        bot_count=0,
        server_type="d",
        platform="l",
        password_protected=True,
        vac_enabled=True,
        edf=1,
        port=2456,
        steam_id=123456,
        stv_port=0,
        stv_name="",
        keywords="",
        game_id=892970,
    )

    async def fake_ainfo(adress, timeout):
        assert adress == ("valheim.test", 2456)
        assert timeout == 3.0
        return fake_info

    monkeypatch.setattr(valheim.a2s, "ainfo", fake_ainfo)

    result = await valheim.check_valheim_server_status(config)

    expected = ValheimServerStatus(
        description="Mein Valheim Server",
        online=True,
        players=4,
        max_players=10,
        latency=42.0,
        version="0.219.16",
        protocol=17,
        map_name="Meadows",
        folder="valheim",
        game="Valheim",
        app_id=892970,
        bot_count=0,
        server_type="d",
        platform="l",
        password_protected=True,
        vac_enabled=True,
        edf=1,
        port=2456,
        steam_id=123456,
        stv_port=0,
        stv_name="",
        keywords="",
        game_id=892970,
    )

    assert result == expected


@pytest.mark.asyncio
async def test_check_valheim_server_status_returns_offline_when_query_fails(
    monkeypatch,
    config,
):

    async def fake_ainfo(adress, timeout):
        assert adress == ("valheim.test", 2456)
        assert timeout == 3.0
        raise TimeoutError("Valheim server antwortet nicht")

    monkeypatch.setattr(valheim.a2s, "ainfo", fake_ainfo)

    result = await valheim.check_valheim_server_status(config)
    assert result.online is False
    assert result.description == "Unknown"
    assert result.players is None
    assert result.max_players is None
    assert result.latency is None

    expected = ValheimServerStatus(
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

    assert result == expected
