from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from common.ai.intelligenceService import get_business_records
from common.analytics.analyticsService import analyze_records, filter_records_by_period
from config.database import get_database
from core.database import get_user_profile
from services.hindsightService import hindsight_service
from services.llmService import llm_service


_fallback_analyses: dict[str, dict[str, Any]] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _collection():
    database = get_database()
    return database['analyses'] if database is not None else None


def generate_analysis(user: dict[str, str], period: str = 'overall') -> dict[str, Any]:
    user_id = user['userId']
    profile = get_user_profile(user_id)
    business_type = profile.get('businessType', 'distributor')
    records = get_business_records(business_type, user_id)
    scoped_records = filter_records_by_period(records, period)
    metrics = analyze_records(business_type, scoped_records)
    memory = hindsight_service.recall_memory({
        'userId': user_id,
        'businessType': business_type,
        'businessName': profile.get('businessName', ''),
        'eventType': 'analysis',
        'query': f'{business_type} {period} operational patterns and prior interventions',
    })
    facts = {
        'business_type': business_type,
        'business_name': profile.get('businessName', ''),
        'period': period,
        'record_count': len(scoped_records),
        'metrics': metrics,
        'current_hotspots': metrics.get('hotspots', []),
        'current_lowspots': metrics.get('lowspots', []),
        'historical_memory': memory if memory.get('status') not in {'fallback', 'error'} else None,
    }
    ai_result = llm_service.generate_recommendation(facts)
    analysis = {
        'analysis_id': str(uuid4()),
        'userId': user_id,
        'businessType': business_type,
        'businessName': profile.get('businessName', ''),
        'createdAt': _now(),
        'period': {'type': period},
        'metrics': metrics,
        'hotspots': metrics.get('hotspots', []),
        'lowspots': metrics.get('lowspots', []),
        'insights': metrics.get('evidence', []),
        'recommendations': [ai_result] if ai_result else [],
        'historical_memory': memory if memory.get('status') not in {'fallback', 'error'} else {
            'status': 'unavailable',
            'message': 'Historical memory currently unavailable.',
        },
        'status': 'generated',
        'applied': False,
    }
    collection = _collection()
    if collection is not None:
        collection.insert_one(analysis.copy())
    else:
        _fallback_analyses[analysis['analysis_id']] = analysis
    return {key: value for key, value in analysis.items() if key != '_id'}


def apply_analysis(analysis_id: str, user: dict[str, str]) -> dict[str, Any] | None:
    collection = _collection()
    query = {'analysis_id': analysis_id, 'userId': user['userId']}
    analysis = collection.find_one(query, {'_id': 0}) if collection is not None else _fallback_analyses.get(analysis_id)
    if not analysis or analysis.get('userId') != user['userId']:
        return None
    applied_at = _now()
    if collection is not None:
        collection.update_one(query, {'$set': {'applied': True, 'appliedAt': applied_at, 'status': 'applied'}})
    else:
        analysis.update({'applied': True, 'appliedAt': applied_at, 'status': 'applied'})
    experience = {
        'userId': user['userId'],
        'businessType': analysis['businessType'],
        'eventType': 'analysis_applied',
        'timestamp': applied_at,
        'situation': analysis['insights'],
        'analysis': analysis['metrics'],
        'action': analysis.get('recommendations', []),
    }
    memory_result = hindsight_service.retain_memory(experience)
    result = dict(analysis)
    result.update({'applied': True, 'appliedAt': applied_at, 'status': 'applied', 'memory_status': memory_result.get('status', 'unknown')})
    return result