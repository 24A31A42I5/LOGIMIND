from core.database import get_user_profile
from services.hindsightService import hindsight_service


def apply_recommendation(recommendation_id: str, user: dict) -> dict:
    profile = get_user_profile(user['userId'])
    intervention = {
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'businessType': profile.get('businessType', 'distributor'),
        'status': 'Applied',
    }
    return intervention


def record_recommendation_outcome(recommendation_id: str, before_minutes: float, after_minutes: float, user: dict) -> dict:
    profile = get_user_profile(user['userId'])
    outcome = 'Successful' if after_minutes < before_minutes else 'Unsuccessful'
    record = {
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'businessType': profile.get('businessType', 'distributor'),
        'eventType': 'recommendation_outcome',
        'before_minutes': before_minutes,
        'after_minutes': after_minutes,
        'outcome': outcome,
    }
    retained = hindsight_service.retain_memory(record)
    record['memory_status'] = retained.get('status', 'unknown')
    return record