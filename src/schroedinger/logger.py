import logging

FORMAT = "%(asctime)s | %(levelname)-8s     | %(name)s -> %(message)s"

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
