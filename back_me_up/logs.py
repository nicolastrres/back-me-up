import logging
import sys
from colorlog import ColoredFormatter  # noqa


def get_logger(name):
    COLORS = {'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'red', }

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_hdlr = logging.StreamHandler(sys.stdout)

    color_formatter = ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s  %(message)s%(reset)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors=COLORS,
    )

    console_hdlr.setFormatter(color_formatter)
    logger.addHandler(console_hdlr)
    return logger
