from dataclasses import dataclass


@dataclass
class ServerStatus:
    description: str
    online: bool
    players: int
    max_players: int
    latency: float
    version: str


@dataclass
class MinecraftServerStatus(ServerStatus):
    is_modded: bool
    modpack: MinecraftModpack | None
    enforces_secure_chat: bool | None
    prevents_chat_reports: bool | None
    protocol_version: int


@dataclass
class MinecraftModpack:
    name: str
    version: str


@dataclass
class ValheimServerStatus(ServerStatus):
    protocol: int
    map_name: str
    folder: str
    game: str
    app_id: int
    bot_count: int
    server_type: str
    platform: str
    password_protected: bool
    vac_enabled: bool
    edf: int
    port: int | None
    steam_id: int | None
    stv_port: int | None
    stv_name: str | None
    keywords: str | None
    game_id: int | None
