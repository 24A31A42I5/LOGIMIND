from __future__ import annotations

from typing import Any, Callable

from common.analytics.analyticsService import analyze_records
from services.hindsightService import hindsight_service
from services.llmService import llm_service


RECORD_SOURCES: dict[str, Callable[[str], list[dict[str, Any]]]] = {}


def _sources() -> dict[str, Callable[[str], list[dict[str, Any]]]]:
    if not RECORD_SOURCES:
        from domains.distributor.service import list_operations
        from domains.raw_material.service import list_supplies
        from domains.restaurant.service import list_orders
        from domains.retail.service import list_sales
        from domains.service_provider.service import list_bookings

        RECORD_SOURCES.update({
            'distributor': list_operations,
            'restaurant': list_orders,
            'raw_material': list_supplies,
            'retail': list_sales,
            'service_provider': list_bookings,
        })
    return RECORD_SOURCES


def get_business_records(business_type: str, user_id: str) -> list[dict[str, Any]]:
    source = _sources().get(business_type)
    return source(user_id) if source else []


def _recommendation_context(business_type: str, metrics: dict[str, Any], historical: str) -> dict[str, Any]:
    top_location = metrics.get('hotspots', [{}])[0].get('location', 'the strongest operating area') if metrics.get('hotspots') else 'the strongest operating area'
    return {
        'business_type': business_type,
        'location': top_location,
        'current_metrics': metrics,
        'historical_evidence': historical,
    }


def generate_intelligence(business_type: str, user_id: str, business_name: str = '') -> dict[str, Any]:
    records = get_business_records(business_type, user_id)
    metrics = analyze_records(business_type, records)
    context = {
        'userId': user_id,
        'businessType': business_type,
        'businessName': business_name,
        'eventType': 'business_intelligence',
        'location': metrics.get('hotspots', [{}])[0].get('location') if metrics.get('hotspots') else None,
    }
    recalled = hindsight_service.recall_memory(context)
    historical_available = recalled.get('status') not in {'fallback', 'error'}
    historical = recalled if historical_available else {'message': 'Historical memory currently unavailable.'}
    facts = _recommendation_context(business_type, metrics, historical)
    llm_result = llm_service.generate_recommendation(facts)
    location = facts['location']
    current_evidence = metrics.get('evidence', [])
    recommendation = llm_result or {
        'title': f'Improve {business_type.replace("_", " ")} capacity in {location}',
        'why': metrics.get('pattern', 'Current demand signals indicate an operational opportunity.'),
        'expected_impact': 'Reduce pressure in the highest-demand operating context.',
        'confidence': min(95, max(45, round(metrics.get('performance', 0) or 60))),
    }
    return {
        'businessType': business_type,
        'businessName': business_name,
        'currentSignals': metrics,
        'detectedPattern': metrics.get('pattern'),
        'currentEvidence': current_evidence,
        'historicalEvidence': historical,
        'insight': metrics.get('insight'),
        'recommendation': recommendation,
        'suggestedAction': recommendation.get('title'),
        'expectedImpact': recommendation.get('expected_impact'),
        'confidence': recommendation.get('confidence', 0),
        'synthetic': True,
    }