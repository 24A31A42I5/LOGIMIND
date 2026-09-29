from services.hindsightService import hindsight_service
from services.seedService import get_demo_store


def apply_recommendation(recommendation_id: str) -> dict:
    store = get_demo_store()
    recommendation = next((item for item in store['recommendations'] if item['id'] == recommendation_id), None)
    if recommendation is None:
        return {'status': 'not_found', 'message': 'Recommendation not found.'}
    recommendation['status'] = 'Applied'
    intervention = {
        'recommendation_id': recommendation_id,
        'area': recommendation['area'],
        'status': 'Applied',
    }
    store.setdefault('interventions', []).append(intervention)
    return intervention


def record_recommendation_outcome(recommendation_id: str, before_minutes: float, after_minutes: float) -> dict:
    store = get_demo_store()
    outcome = 'Successful' if after_minutes < before_minutes else 'Unsuccessful'
    record = {
        'recommendation_id': recommendation_id,
        'before_minutes': before_minutes,
        'after_minutes': after_minutes,
        'outcome': outcome,
    }
    store.setdefault('interventions', []).append(record)
    retained = hindsight_service.retain_memory(record)
    record['memory_status'] = retained.get('status', 'unknown')
    return record