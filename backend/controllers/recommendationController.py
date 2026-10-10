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
        'status': 'approved',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    database = get_database()
    if database is None:
        raise OperationalDataUnavailable('MongoDB is unavailable; operational actions are disabled')
    recommendation = database['recommendations'].find_one({
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'status': 'proposed',
    })
    if recommendation is None:
        raise ValueError('This recommendation is unavailable, already approved, or belongs to another tenant')
    database['recommendations'].update_one(
        {'_id': recommendation['_id']},
        {'$set': {'status': 'approved', 'approved_at': intervention['timestamp']}},
    )
    database['interventions'].insert_one(intervention.copy())
    return intervention


def execute_recommendation(
    recommendation_id: str,
    shipment_id: str,
    agent_id: str,
    user: dict,
) -> dict:
    profile = get_user_profile(user['userId'])
    if profile.get('businessType', 'distributor') != 'distributor':
        raise ValueError('This operational action is currently supported for distributor shipments only')

    database = get_database()
    if database is None:
        raise OperationalDataUnavailable('MongoDB is unavailable; operational actions are disabled')

    intervention = database['interventions'].find_one({
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'status': 'approved',
    })
    if intervention is None:
        raise ValueError('Approve this recommendation before executing the operational action')

    shipment = database['distributor_shipments'].find_one({
        'userId': user['userId'],
        'shipment_id': shipment_id,
    })
    if shipment is None:
        raise ValueError('The shipment was not found in this tenant')

    agent = database['delivery_agents'].find_one({
        'userId': user['userId'],
        'agent_id': agent_id,
    })
    if agent is None:
        raise ValueError('The delivery agent was not found in this tenant')

    executed_at = datetime.now(timezone.utc).isoformat()
    previous_state = {
        'agent_id': shipment.get('agent_id'),
        'status': shipment.get('status'),
    }
    next_state = {
        'agent_id': agent_id,
        'status': 'Assigned',
        'assigned_at': executed_at,
    }
    updated = database['distributor_shipments'].update_one(
        {'_id': shipment['_id'], 'userId': user['userId']},
        {'$set': next_state},
    )
    if updated.matched_count != 1:
        raise ValueError('The shipment changed before the action could be executed')

    execution = {
        'shipment_id': shipment_id,
        'agent_id': agent_id,
        'previous_state': previous_state,
        'next_state': next_state,
        'executed_at': executed_at,
        'actor_user_id': user['userId'],
    }
    database['interventions'].update_one(
        {'_id': intervention['_id']},
        {'$set': {
            'status': 'executed',
            'executed_at': executed_at,
            'execution': execution,
        }},
    )
    database['recommendations'].update_one(
        {
            'recommendation_id': recommendation_id,
            'userId': user['userId'],
            'status': 'approved',
        },
        {'$set': {'status': 'executed', 'executed_at': executed_at}},
    )
    return {
        'recommendation_id': recommendation_id,
        'intervention_id': intervention['intervention_id'],
        'status': 'executed',
        'execution': execution,
    }


def record_recommendation_outcome(
    recommendation_id: str,
    metrics_before: dict[str, Any],
    metrics_after: dict[str, Any],
    notes: str,
    user: dict,
    observation_ids: list[str],
) -> dict:
    profile = get_user_profile(user['userId'])
    database = get_database()
    if database is None:
        raise OperationalDataUnavailable('MongoDB is unavailable; outcomes cannot be verified')
    intervention = database['interventions'].find_one({
        'recommendation_id': recommendation_id,
        'userId': user['userId'],
        'status': 'executed',
    })
    if intervention is None:
        raise ValueError('Execute the approved operational action before recording its outcome')
    collection_name = {
        'distributor': 'distributor_shipments',
        'restaurant': 'restaurant_orders',
        'retail': 'retail_sales',
        'raw_material': 'supplier_orders',
        'service_provider': 'service_bookings',
    }.get(profile.get('businessType', 'distributor'))
    observed = database[collection_name].count_documents({
        'userId': user['userId'],
        '$or': [
            {'id': {'$in': observation_ids}},
            {'record_id': {'$in': observation_ids}},
            {'order_id': {'$in': observation_ids}},
            {'shipment_id': {'$in': observation_ids}},
            {'sale_id': {'$in': observation_ids}},
            {'booking_id': {'$in': observation_ids}},
        ],
    })
    if observed < len(set(observation_ids)):
        raise ValueError('Outcome evidence must reference observed operational records belonging to this tenant')
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