from dataclasses import dataclass


@dataclass
class ServerStatus:
    description: str
    online: bool
    players: int
    max_players: int
    latency: float
    version: str
