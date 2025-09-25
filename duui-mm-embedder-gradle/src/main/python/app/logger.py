import logging
from typing import Optional

__duui_logger: Optional[logging.Logger] = None


def initialize_logger(log_level: str) -> None:
    """
    Initializes a logger for the whole application with the supplied configuration
    :param log_level: Level of logging
    """
    global __duui_logger
    logging.basicConfig(level=log_level)
    __duui_logger = logging.getLogger(__name__)


def get_logger() -> logging.Logger:
    """
    :return:
    A correctly configured and initialized logger
    """
    global __duui_logger

    if __duui_logger is None:
        initialize_logger('INFO')

    return __duui_logger
