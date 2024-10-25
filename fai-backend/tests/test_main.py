from fastapi.testclient import TestClient

from fai_backend.main import app

app.dependency_overrides = {'jwt_access_auth_old': lambda: 'lol'}
client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy'}
