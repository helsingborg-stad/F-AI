import logging


class LoggerConfig:
    """
    A configuration class for the logging module.

    This class configures the logging setup for the Python application by
    specifying the desired logging level and format.

    Attributes:
    -----------
    level : int
        The logging level (e.g., logging.DEBUG, logging.INFO).
    format : str
        The logging message format.

    Methods:
    --------
    configure():
        Applies the logging configurations set by `level` and `format`.
    """

    def __init__(self, level: int, fmt: str):
        self.level = level
        self.format = fmt

    def configure(self):
        logging.basicConfig(
            level=self.level,
            format=self.format
        )
