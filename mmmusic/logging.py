import logging

_logger = None


def get_logger():
    global _logger

    if _logger is None:
        _logger = logging.getLogger(__name__)

        _logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter("[%(asctime)-18s] [%(levelname)s] %(message)s")
        )

        _logger.addHandler(stream_handler)

    return _logger


if __name__ == "__main__":
    logger = get_logger()

    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
