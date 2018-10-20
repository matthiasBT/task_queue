import logging

FORMATTER = logging.Formatter('%(asctime)-15s %(name)-12s: %(levelname)-8s %(message)s')


def get_logger():
    logger = logging.getLogger('api_logger')
    handler = logging.StreamHandler()
    handler.setFormatter(FORMATTER)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


LOGGER = get_logger()
