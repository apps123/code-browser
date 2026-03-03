import logging
from typing import Optional


def configure_logging(level: int = logging.INFO, log_format: Optional[str] = None) -> None:
    """
    Configure basic logging for the CLI and library.

    This should be called once from the CLI entrypoint before other modules run.
    """
    if log_format is None:
        log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    logging.basicConfig(level=level, format=log_format)

