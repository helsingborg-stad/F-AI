from fastapi.testclient import TestClient

from fai_backend.main import app

client = TestClient(app)


def test_greeting_swedish():
    response = client.get('/greet', headers={'language': 'sv'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Hejsan!!!'}
