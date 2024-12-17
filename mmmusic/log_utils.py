from functools import cache
import logging


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
