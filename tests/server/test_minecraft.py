from types import SimpleNamespace

import pytest

from schroedinger.server import minecraft


@pytest.mark.asyncio
async def test_check_mc_server_status_returns_online_status(monkeypatch, config):
    fake_status = SimpleNamespace(
        description="Mein Minecraft Server",
        players=SimpleNamespace(
            online=3,
            max=20,
        ),
        latency=42.7,
        version=SimpleNamespace(
            name="1.21",
            protocol=767,
        ),
        raw={
            "isModded": True,
            "betterStatus": {
                "name": "Mein Modpack",
                "version": "1.0.0",
            },
            "enforcesSecureChat": True,
            "preventsChatReports": False,
        },
    )

    class FakeJavaServer:
        def __init__(self, host, port) -> None:
            assert host == "minecraft.test"
            assert port == 25565

        async def async_status(self):
            return fake_status

    monkeypatch.setattr(minecraft, "JavaServer", FakeJavaServer)

    result = await minecraft.check_mc_server_status(config)

    assert result.online is True
    assert result.description == "Mein Minecraft Server"
    assert result.players == 3
    assert result.max_players == 20
    assert result.latency == 42.7
    assert result.version == "1.21"
    assert result.is_modded is True
    assert result.modpack == minecraft.MinecraftModpack(
        name="Mein Modpack", version="1.0.0"
    )
    assert result.enforces_secure_chat is True
    assert result.prevents_chat_reports is False
    assert result.protocol_version == 767


@pytest.mark.asyncio
async def test_check_mc_server_status_returns_offline_when_query_fails(
    monkeypatch,
    config,
):
    class FakeJavaServer:
        def __init__(self, host, port) -> None:
            assert host == "minecraft.test"
            assert port == 25565

        async def async_status(self):
            raise TimeoutError("Minecraft server antwortet nicht")

    monkeypatch.setattr(minecraft, "JavaServer", FakeJavaServer)

    result = await minecraft.check_mc_server_status(config)

    assert result.description == "Unknown"
    assert result.online is False
    assert result.players is None
    assert result.max_players is None
    assert result.latency is None
    assert result.version == "Unknown"
    assert result.is_modded is None
    assert result.modpack is None
    assert result.enforces_secure_chat is None
    assert result.protocol_version == 0
    assert result.prevents_chat_reports is None
