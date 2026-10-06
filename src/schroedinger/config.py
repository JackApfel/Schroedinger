import logging
import os
from dataclasses import dataclass

import dotenv

logger = logging.getLogger(__name__)

dotenv.load_dotenv()


@dataclass
class Config:
    token: str
    minecraft_host_ip: str
    minecraft_port: int
    valheim_host_ip: str
    valheim_port: int
    hytale_host_ip: str
    hytale_port: int


def _required(name: str, label: str) -> str:
    value = os.getenv(name)

    if value is None:
        raise ValueError(f"{label} not found in environment variables.")

    return value


def _port(name: str, label: str) -> int:
    value = _required(name, label)

    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"{label} must be an integer.") from error


def load_config() -> Config:
    return Config(
        token=_required("TOKEN", "Discord Token"),
        minecraft_host_ip=_required("MINECRAFT_HOST_IP", "Minecraft Host IP"),
        minecraft_port=_port("MINECRAFT_PORT", "Minecraft Port"),
        valheim_host_ip=_required("VALHEIM_HOST_IP", "Valheim Host IP"),
        valheim_port=_port("VALHEIM_PORT", "Valheim Port"),
        hytale_host_ip=_required("HYTALE_HOST_IP", "Hytale Host IP"),
        hytale_port=_port("HYTALE_PORT", "Hytale Port"),
    )
