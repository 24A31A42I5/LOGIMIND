from services.hindsightService import hindsight_service
from services.logisticsAgent import close_day_summary
from services.mongoRebuildService import rebuild_linked_database
from services.seedService import get_demo_store, reset_demo_store


def load_demo_day(day: int) -> dict:
    store = get_demo_store()
    store['active_day'] = max(1, min(day, 30))
    return {'day': store['active_day'], 'message': f'Demo data loaded for day {store["active_day"]}.'}


def trigger_area_c_delay() -> dict:
    store = get_demo_store()
    targets = [item for item in store['shipments'] if item['area'] == 'Area C'][:3]
    for shipment in targets:
        shipment['status'] = 'Delayed'
        shipment['delay_minutes'] = max(shipment['delay_minutes'], 20)
    return {'updated_shipments': len(targets), 'message': 'Area C delay hotspot triggered.'}


def trigger_failed_delivery() -> dict:
    store = get_demo_store()
    target = next((item for item in store['shipments'] if item['area'] == 'Area D'), None)
    if target:
        target['status'] = 'Failed'
        target['delay_minutes'] = max(target['delay_minutes'], 30)
    return {'updated_shipments': 1 if target else 0, 'message': 'Failed-delivery hotspot triggered.'}


def trigger_successful_intervention() -> dict:
    store = get_demo_store()
    target = next((item for item in store['recommendations'] if item['id'] == 'rec-001'), None)
    if target:
        target['status'] = 'Applied'
    store.setdefault('interventions', []).append({
        'recommendation_id': 'rec-001',
        'area': 'Area C',
        'before_minutes': 48,
        'after_minutes': 31,
        'outcome': 'Successful',
    })
    return {'status': 'Successful', 'before_minutes': 48, 'after_minutes': 31, 'message': 'Successful intervention recorded.'}


def reset_demo() -> dict:
    reset_demo_store()
    return {'status': 'reset', 'message': 'Demo data reset.'}


def close_demo_day() -> dict:
    summary = close_day_summary()
    retained = hindsight_service.retain_memory(summary)
    summary['memory_status'] = retained.get('status', 'unknown')
    if retained.get('status') == 'fallback':
        summary['message'] = 'Historical memory currently unavailable; day summary was not retained.'
    return summary


def seed_demo_database() -> dict:
    return rebuild_linked_database()


def rebuild_demo_database() -> dict:
    return rebuild_linked_database()