import logging
import sys
from typing import Any


def setup_logging(verbose: bool) -> None:
    """Set up logging configuration.

    Args:
        verbose (bool): If True, set logging level to DEBUG.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def log_exception(exc: Exception, message: str = "") -> None:
    """Log an exception with an optional message.

    Args:
        exc (Exception): The exception to log.
        message (str, optional): Additional message. Defaults to "".
    """
    logging.error(f"{message}: {exc}")
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.exception(exc)