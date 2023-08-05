# Enable logging for "requests"
from typing import Optional

import logging

from http.client import HTTPConnection

from dnastack.feature_flags import in_global_debug_mode

logging_format = '[%(levelname)s] %(name)s: %(message)s'
default_logging_level = logging.INFO

if in_global_debug_mode:
    default_logging_level = logging.DEBUG
    logging.basicConfig(format=logging_format,
                        level=default_logging_level)
    HTTPConnection.debuglevel = 1

# Configure the logger of HTTP client (global settings)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(default_logging_level)
requests_log.propagate = True


def get_logger(name: str, level: Optional[int] = None):
    formatter = logging.Formatter(logging_format)

    handler = logging.StreamHandler()
    handler.setLevel(level or default_logging_level)
    handler.setFormatter(formatter)

    logger = logging.Logger(name)
    logger.setLevel(level or default_logging_level)
    logger.addHandler(handler)

    return logger
