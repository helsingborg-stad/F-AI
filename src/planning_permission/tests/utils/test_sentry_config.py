import unittest
import logging

import sentry_sdk

from planning_permission.utils.sentry_config import SentryConfig


def fake_sentry_init(dsn=None, integrations=None, traces_sample_rate=None):
    return dsn, integrations, traces_sample_rate


class TestSentryConfig(unittest.TestCase):
    def test_level_setting(self):
        sentry_sdk.init = fake_sentry_init

        dsn = 'https://0000@sentry.test.com/1'
        config = SentryConfig(dsn, level='WARNING', event_level='INFO', trace_sample_rate=1.0)

        config.initialize()
        current_config = config.get_config()

        assert current_config['level'] == logging.WARNING
        assert current_config['event_level'] == logging.INFO
        assert current_config['trace_sample_rate'] == 1.0

    def test_default_settings(self):
        sentry_sdk.init = fake_sentry_init
        dsn = 'https://0000@sentry.test.com/1'
        config_default = SentryConfig(dsn)
        config_default.initialize()
        current_config_default = config_default.get_config()

        assert current_config_default['level'] == logging.ERROR
        assert current_config_default['event_level'] == logging.ERROR
        assert current_config_default['trace_sample_rate'] == 0.0


if __name__ == '__main__':
    unittest.main()
