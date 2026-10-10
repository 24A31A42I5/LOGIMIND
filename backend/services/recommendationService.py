from typing import Any

from common.ai.intelligenceService import generate_intelligence, get_business_records
from common.analytics.analyticsService import analyze_records
from common.repository import domain_records_are_persisted


def _data_source_for(business_type: str, user_id: str) -> str:
    collection_name = {
        'distributor': 'distributor_shipments',
        'restaurant': 'restaurant_orders',
        'raw_material': 'supplier_orders',
        'retail': 'retail_sales',
        'service_provider': 'service_bookings',
    }.get(business_type, 'distributor_shipments')
    return 'mongodb' if domain_records_are_persisted(collection_name, user_id) else 'no_data'


def generate_investigation(area: str | None = None, business_type: str = 'distributor', user_id: str = 'demo', business_name: str = '') -> dict[str, Any]:
    intelligence = generate_intelligence(business_type, user_id, business_name)
    recommendation = {
        **intelligence['recommendation'],
        'current_evidence': intelligence['currentEvidence'],
        'historical_memory': intelligence['historicalEvidence'],
    }
    data_source = intelligence.get('data_source') or _data_source_for(business_type, user_id)
    pattern_area = area or intelligence.get('currentSignals', {}).get('hotspots', [{}])[0].get('location') or 'Area C'
    return {
        'area': pattern_area,
        'summary': intelligence['insight'],
        'recommendations': [recommendation],
        'memory_available': intelligence['historicalEvidence'].get('status') not in {'fallback', 'error'},
        'llm_used': bool(intelligence.get('recommendation')),
        'data_source': data_source,
        'synthetic': False,
        **intelligence,
    }


def get_today_insights(business_type: str = 'distributor', user_id: str = 'demo') -> dict[str, Any]:
    metrics = analyze_records(business_type, get_business_records(business_type, user_id))
    data_source = _data_source_for(business_type, user_id)
    return {'summary': metrics['insight'], 'insights': metrics['evidence'], 'businessType': business_type, 'synthetic': False, 'data_source': data_source}
