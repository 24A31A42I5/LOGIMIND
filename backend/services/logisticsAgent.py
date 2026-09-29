from __future__ import annotations

from services.seedService import get_demo_store


def get_active_agents() -> list[dict]:
    return get_demo_store()['delivery_agents']


def close_day_summary() -> dict:
    store = get_demo_store()
    shipments = store['shipments']
    delivered = sum(1 for item in shipments if item['status'] == 'Delivered')
    delayed = sum(1 for item in shipments if item['status'] in {'Delayed', 'Failed'})
    avg = round(sum(item['duration_minutes'] for item in shipments) / len(shipments), 2) if shipments else 0
    return {
        'day': 'August 30',
        'total_shipments': len(shipments),
        'delivered': delivered,
        'delayed': delayed,
        'average_delivery_time': avg,
        'message': "Today's operational experience has been added to organizational memory.",
    }
