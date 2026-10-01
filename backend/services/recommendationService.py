from typing import Any

from common.ai.intelligenceService import generate_intelligence, get_business_records
from common.analytics.analyticsService import analyze_records
from core.database import get_user_profile
from services.hindsightService import hindsight_service


def generate_investigation(area: str | None = None, business_type: str = 'distributor', user_id: str = 'demo', business_name: str = '') -> dict[str, Any]:
    intelligence = generate_intelligence(business_type, user_id, business_name)
    recommendation = {**intelligence['recommendation'], 'current_evidence': intelligence['currentEvidence'], 'historical_memory': intelligence['historicalEvidence']}
    return {
        'area': area or (intelligence['currentSignals'].get('hotspots') or [{}])[0].get('location'),
        'summary': intelligence['insight'],
        'recommendations': [recommendation],
        'memory_available': intelligence['historicalEvidence'].get('status') not in {'fallback', 'error'},
        'llm_used': intelligence['recommendation'] != {},
        **intelligence,
    }


def get_today_insights(business_type: str = 'distributor', user_id: str = 'demo') -> dict[str, Any]:
    metrics = analyze_records(business_type, get_business_records(business_type, user_id))
    return {'summary': metrics['insight'], 'insights': metrics['evidence'], 'businessType': business_type, 'synthetic': True}
