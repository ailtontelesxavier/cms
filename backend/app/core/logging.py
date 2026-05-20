import sys

from loguru import logger


def setup_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {extra[request_id]:<36} | {message}",
        level="INFO",
        filter=lambda record: "request_id" in record["extra"],
    )
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {message}",
        level="DEBUG" if __debug__ else "INFO",
    )
