import logging
import os
import sys
import dotenv

logger = logging.getLogger(__name__)

dotenv.load_dotenv()


TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    logger.error("Discord Token not found in environment variables.")
    sys.exit(1)

MINECRAFT_HOST_IP = os.getenv("MINECRAFT_HOST_IP")
if MINECRAFT_HOST_IP is None:
    logger.error("Minecraft Host IP not found in environment variables.")
    sys.exit(1)

MINECRAFT_PORT = os.getenv("MINECRAFT_PORT")
if MINECRAFT_PORT is None:
    logger.error("Minecraft Port not found in environment variables.")
    sys.exit(1)

try:
    MINECRAFT_PORT = int(MINECRAFT_PORT)
except ValueError:
    logger.error("Minecraft Port must be an integer.")
    sys.exit(1)

VALHEIM_HOST_IP = os.getenv("VALHEIM_HOST_IP")
if VALHEIM_HOST_IP is None:
    logger.error("Valheim Host IP not found in environment variables.")
    sys.exit(1)

VALHEIM_PORT = os.getenv("VALHEIM_PORT")
if VALHEIM_PORT is None:
    logger.error("Valheim Port not found in environment variables.")
    sys.exit(1)

try:
    VALHEIM_PORT = int(VALHEIM_PORT)
except ValueError:
    logger.error("Valheim Port must be an integer.")
    sys.exit(1)
