import pytest

from fai_llm.app_life.service import AppLifeService
from fai_llm.config.service import settings
from fai_llm.log.service import MPLogging
from fai_llm.service_locator.service import global_locator


def setup_global_locator():
    settings.LOG_FILE = False
    settings.LOG_STDOUT = False
    global_locator.services.main_logger = MPLogging.get_logger('test')
    global_locator.services.app_life = AppLifeService()
    return global_locator
