from src.modules.llm.helpers.parse_model_key import parse_model_key


def test_model_key():
    result = parse_model_key('my-provider:my-model')

    assert result[0] == 'my-provider'
    assert result[1] == 'my-model'


def test_model_key_invalid():
    result = parse_model_key('my-key')

    assert result[0] == 'my-key'
    assert result[1] == 'my-key'
