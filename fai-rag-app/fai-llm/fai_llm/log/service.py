import logging
import sys
from typing import Self

from ..config.service import settings


class ScopeableLogger(logging.Logger):
    def scope(self, name: str) -> Self:
        new_logger = ScopeableLogger(f'{self.name}.{name}')
        new_logger.setLevel(self.level)
        for handler in self.handlers:
            new_logger.addHandler(handler)
        return new_logger


class MPLogging:
    _loggers: dict[str, ScopeableLogger] = {}

    @staticmethod
    def get_logger(name: str) -> ScopeableLogger:
        if name in MPLogging._loggers:
            return MPLogging._loggers[name]

        new_logger = MPLogging._create_logger(name)
        MPLogging._loggers[name] = new_logger
        return new_logger

    @staticmethod
    def _create_logger(name) -> ScopeableLogger:
        new_logger = ScopeableLogger(name)
        log_level = logging.getLevelNamesMapping()[settings.LOG_LEVEL.upper()]
        new_logger.setLevel(log_level)

        formatter = logging.Formatter(settings.LOG_FORMAT)

        if settings.LOG_FILE:
            file_handler = logging.FileHandler(f'{name}.log')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            new_logger.addHandler(file_handler)

        if settings.LOG_STDOUT:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(log_level)
            stdout_handler.setFormatter(formatter)
            new_logger.addHandler(stdout_handler)

        return new_logger
