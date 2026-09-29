from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_investigation_endpoint_returns_recommendations():
    response = client.post('/api/insights/investigate', json={'area': 'Area C'})
    assert response.status_code == 200
    payload = response.json()
    assert 'area' in payload
    assert 'summary' in payload
    assert 'recommendations' in payload
    assert isinstance(payload['recommendations'], list)
