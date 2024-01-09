import logging

import bcrypt
from rich.logging import RichHandler

from fai_backend.logger.console import console


def setup_logger():
    logging.basicConfig(
        level="DEBUG",
        format=" %(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                show_time=False, console=console, tracebacks_suppress=[bcrypt._bcrypt]
            )
        ],
    )

    return logging.getLogger("rich")
