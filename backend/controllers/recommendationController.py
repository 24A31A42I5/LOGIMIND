from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from config.database import get_database
from core.database import get_user_profile
from services.hindsightService import hindsight_service


_fallback_interventions: dict[str, dict[str, Any]] = {}
_fallback_outcomes: dict[str, dict[str, Any]] = {}


def apply_recommendation(recommendation_id: str, user: dict) -> dict:
    profile = get_user_profile(user['userId'])
    intervention = {
        'intervention_id': str(uuid4()),
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'businessType': profile.get('businessType', 'distributor'),
        'action': recommendation_id,
        'status': 'applied',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    database = get_database()
    if database is not None:
        database['interventions'].insert_one(intervention.copy())
    else:
        _fallback_interventions[intervention['intervention_id']] = intervention
    return intervention


def record_recommendation_outcome(recommendation_id: str, metrics_before: dict[str, Any], metrics_after: dict[str, Any], notes: str, user: dict) -> dict:
    profile = get_user_profile(user['userId'])
    before_score = sum(float(value) for value in metrics_before.values() if isinstance(value, (int, float)))
    after_score = sum(float(value) for value in metrics_after.values() if isinstance(value, (int, float)))
    outcome = 'successful' if before_score and after_score < before_score else 'recorded'
    record = {
        'outcome_id': str(uuid4()),
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'businessType': profile.get('businessType', 'distributor'),
        'eventType': 'recommendation_outcome',
        'metrics_before': metrics_before,
        'metrics_after': metrics_after,
        'outcome': outcome,
        'notes': notes,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    database = get_database()
    if database is not None:
        database['outcomes'].insert_one(record.copy())
    else:
        _fallback_outcomes[record['outcome_id']] = record
    retained = hindsight_service.retain_memory(record)
    record['memory_status'] = retained.get('status', 'unknown')
    return record