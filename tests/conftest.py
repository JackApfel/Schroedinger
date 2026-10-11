import pytest

from schroedinger.config import Config
from schroedinger.models import server_status as schroedinger_server_status


@pytest.fixture
def config():
    return Config(
        token="test-token",
        minecraft_host_ip="minecraft.test",
        minecraft_port=25565,
        valheim_host_ip="valheim.test",
        valheim_port=2456,
        hytale_host_ip="hytale.test",
        hytale_port=5520,
    )


@pytest.fixture
def server_status():
    return schroedinger_server_status.ServerStatus(
        description="Mein Server",
        online=True,
        players=3,
        max_players=20,
        latency=42.7,
        version="1.21",
    )


@pytest.fixture
def empty_server_status():
    return schroedinger_server_status.ServerStatus(
        description=None,
        online=None,
        players=None,
        max_players=None,
        latency=None,
        version=None,
    )
