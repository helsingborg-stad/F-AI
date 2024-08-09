from unittest.mock import Mock

from fai_llm.app_life.service import AppLifeService


def test_service():
    mock_callback = Mock()
    app_life = AppLifeService()

    app_life.add_on_shutdown(mock_callback)
    app_life.shutdown()

    assert mock_callback.call_count == 1
