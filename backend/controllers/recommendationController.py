from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from config.database import get_database
from common.repository import OperationalDataUnavailable
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
    if database is None:
        raise OperationalDataUnavailable('MongoDB is unavailable; operational actions are disabled')
    database['interventions'].insert_one(intervention.copy())
    return intervention


def record_recommendation_outcome(recommendation_id: str, metrics_before: dict[str, Any], metrics_after: dict[str, Any], notes: str, user: dict) -> dict:
    profile = get_user_profile(user['userId'])
    database = get_database()
    if database is None:
        raise OperationalDataUnavailable('MongoDB is unavailable; outcomes cannot be verified')
    intervention = database['interventions'].find_one({
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'status': 'applied',
    })
    if intervention is None:
        raise ValueError('Record the approved operational action before recording its outcome')
    comparable = set(metrics_before) & set(metrics_after)
    if not comparable or any(not isinstance(metrics_before[key], (int, float)) or not isinstance(metrics_after[key], (int, float)) for key in comparable):
        raise ValueError('Provide at least one comparable numeric metric before and after the action')
    lower_is_better = any(token in key.lower() for key in comparable for token in ('time', 'delay', 'stockout', 'backlog', 'cost', 'travel'))
    if lower_is_better:
        outcome = 'successful' if all(metrics_after[key] < metrics_before[key] for key in comparable) else 'declined' if any(metrics_after[key] > metrics_before[key] for key in comparable) else 'inconclusive'
    else:
        outcome = 'successful' if all(metrics_after[key] > metrics_before[key] for key in comparable) else 'declined' if any(metrics_after[key] < metrics_before[key] for key in comparable) else 'inconclusive'
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
    database['outcomes'].insert_one(record.copy())
    retained = hindsight_service.retain_memory(record) if outcome == 'successful' else {'status': 'not_retained', 'message': 'Outcome did not meet retention criteria.'}
    record['memory_status'] = retained.get('status', 'unknown')
    return record