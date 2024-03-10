from functools import cache
import logging
import os

# Set the log level to DEBUG for all loggers if running in debug mode.
if os.getenv("DEBUG") == "true":
    logging.basicConfig(level="DEBUG")


@cache
def get_logger():
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("[%(asctime)-18s] [%(levelname)s] %(message)s")
    )

    logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger()

    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
