from fastapi.testclient import TestClient

from fai_backend.main import app
from fai_backend.phrase import Phrase, language_mappings, phrase

client = TestClient(app)


def test_greeting_english():
    response = client.get('/greet', headers={'language': 'en'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello'}


def test_greeting_swedish():
    response = client.get('/greet', headers={'language': 'sv'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hej'}


def test_greeting_default_language():
    response = client.get('/greet')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello'}


def test_greeting_nonexistent_key():
    phrase.set_language('en')
    assert phrase('nonexistent') == 'nonexistent'


def test_invalid_language_code():
    phrase.set_language('xyz')  # Set an invalid language code
    assert phrase('greeting', 'Default Greeting') == 'Hello', 'Should fallback to English for invalid language code'


def test_non_string_key():
    try:
        phrase(123, 'Default')  # Non-string key
        assert False, 'TypeError expected for non-string key'
    except TypeError:
        assert True


def test_non_string_default():
    try:
        phrase('greeting', 123)  # Non-string default value
        assert False, 'TypeError expected for non-string default value'
    except TypeError:
        assert True


def test_configurable_default_language():
    test_default_lang = 'sv'  # Swedish for testing
    test_phrase = Phrase(language_mappings, test_default_lang)
    test_phrase.set_language('xyz')  # Invalid language to trigger default
    assert test_phrase('greeting', 'Default Greeting') == 'Hej', 'Should use Swedish as the default language'
