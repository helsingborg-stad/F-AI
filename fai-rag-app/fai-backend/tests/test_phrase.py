from fastapi.testclient import TestClient

from fai_backend.auth.security import authenticate
from fai_backend.main import app
from fai_backend.phrase import phrase, set_language

client = TestClient(app)


def authenticate_override():
    return True


app.dependency_overrides[authenticate] = authenticate_override


def test_greeting_swedish():
    response = client.get('/greet', headers={'language': 'sv'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hej'}


def test_greeting_nonexistent_key():
    set_language('en')
    assert phrase('nonexistent') == 'nonexistent'


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
    set_language('xyz')  # Invalid language to trigger default
    assert phrase('greeting', 'Default Greeting') == 'Hej', 'Should use Swedish as the default language'


def test_placeholders_happy():
    assert phrase('hello_key', 'Hello {name}', name='Rambo') == 'Hello Rambo'
