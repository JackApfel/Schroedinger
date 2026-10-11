import pytest

from schroedinger.config import Config, load_config


def test_load_config(monkeypatch):
    monkeypatch.setenv("TOKEN", "test-token")
    monkeypatch.setenv("MINECRAFT_HOST_IP", "minecraft.test")
    monkeypatch.setenv("MINECRAFT_PORT", "25565")
    monkeypatch.setenv("VALHEIM_HOST_IP", "valheim.test")
    monkeypatch.setenv("VALHEIM_PORT", "2456")
    monkeypatch.setenv("HYTALE_HOST_IP", "hytale.test")
    monkeypatch.setenv("HYTALE_PORT", "5520")
    config = load_config()

    expected = Config(
        token="test-token",
        minecraft_host_ip="minecraft.test",
        minecraft_port=25565,
        valheim_host_ip="valheim.test",
        valheim_port=2456,
        hytale_host_ip="hytale.test",
        hytale_port=5520,
    )
    assert config == expected


def test_load_config_raise_for_invalid_port(monkeypatch):
    monkeypatch.setenv("TOKEN", "test-token")
    monkeypatch.setenv("MINECRAFT_HOST_IP", "minecraft.test")
    monkeypatch.setenv("MINECRAFT_PORT", "kein-port")
    monkeypatch.setenv("VALHEIM_HOST_IP", "valheim.test")
    monkeypatch.setenv("VALHEIM_PORT", "2456")
    monkeypatch.setenv("HYTALE_HOST_IP", "hytale.test")
    monkeypatch.setenv("HYTALE_PORT", "5520")

    with pytest.raises(ValueError, match="Minecraft Port must be an integer"):
        load_config()


def test_load_config_raise_for_invalid_required(monkeypatch):
    monkeypatch.setenv("TOKEN", "test-token")
    monkeypatch.delenv("MINECRAFT_HOST_IP", raising=False)
    monkeypatch.setenv("MINECRAFT_PORT", "25565")
    monkeypatch.setenv("VALHEIM_HOST_IP", "valheim.test")
    monkeypatch.setenv("VALHEIM_PORT", "2456")
    monkeypatch.setenv("HYTALE_HOST_IP", "hytale.test")
    monkeypatch.setenv("HYTALE_PORT", "5520")

    with pytest.raises(
        ValueError, match="Minecraft Host IP not found in environment variables."
    ):
        load_config()
