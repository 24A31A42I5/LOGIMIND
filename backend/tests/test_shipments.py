from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shipments_endpoint_returns_data():
    response = client.get('/api/shipments')
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) > 0
    assert 'shipment_id' in payload[0] or 'id' in payload[0]


def test_single_shipment_endpoint():
    first_id = client.get('/api/shipments').json()[0]['shipment_id']
    response = client.get(f'/api/shipments/{first_id}')
    assert response.status_code == 200
    payload = response.json()
    assert payload['shipment_id'] == first_id
