# Schroedinger

Ein kleiner Discord-Bot zum Überprüfen von Server-Status.

![Abbildung vom /status all Befehl](image.png)

---

## Requirements

- Python >=3.14
- [uv](https://docs.astral.sh/uv/)

## Installation

### Setup

```bash
git clone https://github.com/JackApfel/Schroedinger.git
cd Schroedinger
uv sync
```

### Configuration

Erstelle und konfiguriere eine `.env` im Projektverzeichnis.
`.env.example` dient als Vorlage.

```bash
cp .env.example .env
```

```env
TOKEN=Discord Bot Token

MINECRAFT_HOST_IP=IP vom Minecraft Server
MINECRAFT_PORT=Port vom Minecraft Server

VALHEIM_HOST_IP=IP vom Valheim Server
VALHEIM_PORT=Port vom Valheim Server
```

### Ausführen

```bash
uv run schroedinger
```