import aiohttp
import pytest
from aiohttp import ClientTimeout

from schroedinger.models.server_status import HytaleServerStatus
from schroedinger.server import hytale


@pytest.mark.asyncio
async def test_check_hytale_server_status_returns_online_status(
    monkeypatch,
    config,
):
    fake_status = {
        "Server": {
            "Name": "Hytale Server",
            "Version": "0.6.8",
            "Revision": "d2feeb3997f2efc9b4fe23282a3ece38f0618047",
            "Patchline": "release",
            "ProtocolVersion": 2,
            "ProtocolHash": "-1356075162",
            "ProtocolCrc": -1356075162,
            "MaxPlayers": 100,
        },
        "Universe": {
            "CurrentPlayers": 1,
            "DefaultWorld": "default",
        },
        "Players": [
            {
                "Name": "User",
                "UUID": "dcd5dd40-cbc4-4a71-848e-cc3281b53g43f",
                "World": "default",
            }
        ],
    }

    class FakeResponse:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return False

        def raise_for_status(self):
            pass

        async def json(self):
            return fake_status

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return False

        def get(self, url, ssl, timeout):
            assert url == (
                f"https://{config.hytale_host_ip}:"
                f"{config.hytale_port + 3}/Nitrado/Query"
            )
            assert ssl is False
            assert timeout == ClientTimeout(3.0)

            return FakeResponse()

    monkeypatch.setattr(hytale.aiohttp, "ClientSession", FakeSession)

    status = await hytale.check_hytale_server_status(config)

    assert status == HytaleServerStatus(
        description="Hytale Server",
        online=True,
        max_players=100,
        players=1,
        latency=status.latency,
        version="0.6.8",
        default_world="default",
    )


@pytest.mark.asyncio
async def test_check_hytale_server_status_returns_offline_status(
    monkeypatch,
    config,
):
    fake_status = {}

    class FakeResponse:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return False

        def raise_for_status(self):
            raise Exception(aiohttp.ClientConnectorError)

        async def json(self):
            return fake_status

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return False

        def get(self, url, ssl, timeout):
            assert url == (
                f"https://{config.hytale_host_ip}:"
                f"{config.hytale_port + 3}/Nitrado/Query"
            )
            assert ssl is False
            assert timeout == ClientTimeout(3.0)

            return FakeResponse()

    monkeypatch.setattr(hytale.aiohttp, "ClientSession", FakeSession)

    status = await hytale.check_hytale_server_status(config)

    assert status == HytaleServerStatus(
        description=None,
        online=False,
        max_players=None,
        players=None,
        latency=None,
        version=None,
        default_world=None,
    )
