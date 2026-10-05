from dataclasses import dataclass


@dataclass
class ServerStatus:
    description: str | None
    online: bool | None
    players: int | None
    max_players: int | None
    latency: float | None
    version: str | None


@dataclass
class MinecraftServerStatus(ServerStatus):
    is_modded: bool | None
    modpack: MinecraftModpack | None
    enforces_secure_chat: bool | None
    prevents_chat_reports: bool | None
    protocol_version: int | None


@dataclass
class MinecraftModpack:
    name: str
    version: str


@dataclass
class ValheimServerStatus(ServerStatus):
    protocol: int | None
    map_name: str | None
    folder: str | None
    game: str | None
    app_id: int | None
    bot_count: int | None
    server_type: str | None
    platform: str | None
    password_protected: bool | None
    vac_enabled: bool | None
    edf: int | None
    port: int | None
    steam_id: int | None
    stv_port: int | None
    stv_name: str | None
    keywords: str | None
    game_id: int | None


@dataclass
class HytaleServerStatus(ServerStatus):
    default_world: str | None
