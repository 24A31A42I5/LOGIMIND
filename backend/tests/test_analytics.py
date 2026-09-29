from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_overall_analytics_endpoint():
    response = client.get('/api/analytics/overall')
    assert response.status_code == 200
    payload = response.json()
    assert 'total_deliveries' in payload
    assert 'delay_rate' in payload
    assert 'area_hotspots' in payload
    assert isinstance(payload['area_hotspots'], list)


def test_daily_analytics_endpoint():
    response = client.get('/api/analytics/daily')
    assert response.status_code == 200
    payload = response.json()
    assert 'today' in payload or 'daily' in payload
    assert isinstance(payload.get('timeline', payload.get('daily', [])), list)
