import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


class SentryConfig:
    """
    A class to configure and initialize Sentry integration for a Python application.

    Attributes:
    -----------
    dns : str
        The Sentry DSN (Data Source Name) pointing to the Sentry project.
    level : int
        The minimum logging level at which logs should be captured.
    event_level : int
        The minimum logging level at which logs should be sent as events to Sentry.
    trace_sample_rate : float
        The rate at which traces should be sampled and sent to Sentry. Range [0.0, 1.0].

    Methods:
    --------
    initialize():
        Initializes the Sentry SDK with the provided configuration.
    get_config() -> dict[str, str]:
        Returns the current Sentry configuration.
    """

    def __init__(self, dns: str, level='ERROR', event_level='ERROR', trace_sample_rate=0.0) -> None:
        self.dns = dns
        self.level = logging.getLevelName(level)
        self.event_level = logging.getLevelName(event_level)
        self.trace_sample_rate = trace_sample_rate

    def initialize(self) -> None:
        sentry_logging = LoggingIntegration(
            level=self.level,
            event_level=self.event_level
        )

        sentry_sdk.init(
            dsn=self.dns,
            integrations=[sentry_logging],
            traces_sample_rate=self.trace_sample_rate
        )

    def get_config(self) -> dict[str, str]:
        """Return the current Sentry configuration."""
        return {
            "dsn": self.dns,
            "level": self.level,
            "event_level": self.event_level,
            "trace_sample_rate": self.trace_sample_rate
        }
