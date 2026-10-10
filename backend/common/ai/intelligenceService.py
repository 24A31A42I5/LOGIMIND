from __future__ import annotations

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


def _data_source(records: list[dict[str, Any]]) -> str:
    if not records:
        return 'no_data'
    return 'mongodb'


def _time_window_from_records(records: list[dict[str, Any]]) -> str:
    hours = []
    for record in records:
        for key in ('dispatch_time', 'timestamp', 'order_time', 'start_time'):
            value = record.get(key)
            if not value:
                continue
            try:
                hours.append(int(str(value)[11:13]))
            except (TypeError, ValueError, IndexError):
                continue
    if not hours:
        return 'observed operating hours'
    lower = min(hours)
    upper = max(hours)
    return f'{lower:02d}:00-{upper:02d}:00'


def _pattern_for_business(business_type: str, records: list[dict[str, Any]], metrics: dict[str, Any]) -> dict[str, Any]:
    if business_type != 'distributor' or not records:
        return {
            'area': metrics.get('hotspots', [{}])[0].get('location') if metrics.get('hotspots') else None,
            'time_window': _time_window_from_records(records),
            'delivery_volume': len(records),
            'average_delivery_duration_minutes': metrics.get('currentData', {}).get('performance') if metrics.get('currentData') else None,
            'delay_rate': None,
            'delivery_agent_workload': len({record.get('agent_id') for record in records if record.get('agent_id')}) or None,
            'recurrence_across_dates': len({str(item.get('timestamp', '')).split('T')[0] for item in records if item.get('timestamp')}) or None,
        }

    by_area: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        area = str(record.get('area') or record.get('location') or 'Unknown')
        by_area.setdefault(area, []).append(record)

    if not by_area:
        return {'area': None, 'time_window': _time_window_from_records(records), 'delivery_volume': len(records), 'average_delivery_duration_minutes': None, 'delay_rate': None, 'delivery_agent_workload': None, 'recurrence_across_dates': None}

    area_name, area_records = sorted(by_area.items(), key=lambda item: len(item[1]), reverse=True)[0]
    delays = [record for record in area_records if record.get('status') in {'Delayed', 'Failed'}]
    average_duration = round(sum(float(record.get('duration_minutes', 0) or 0) for record in area_records) / max(1, len(area_records)), 2)
    delay_rate = round(len(delays) / max(1, len(area_records)), 4)
    time_window = _time_window_from_records(area_records)
    return {
        'area': area_name,
        'time_window': time_window,
        'delivery_volume': len(area_records),
        'average_delivery_duration_minutes': average_duration,
        'delay_rate': delay_rate,
        'delivery_agent_workload': max(1, len({record.get('agent_id') for record in area_records if record.get('agent_id')})),
        'recurrence_across_dates': len({str(item.get('timestamp', '')).split('T')[0] for item in area_records if item.get('timestamp')}),
        'data_source': _data_source(area_records),
    }


def get_business_records(business_type: str, user_id: str) -> list[dict[str, Any]]:
    source = _sources().get(business_type)
    return source(user_id) if source else []


def _recommendation_context(business_type: str, metrics: dict[str, Any], historical: str) -> dict[str, Any]:
    top_location = metrics.get('hotspots', [{}])[0].get('location') if metrics.get('hotspots') else None
    return {
        'business_type': business_type,
        'location': top_location,
        'current_metrics': metrics,
        'historical_evidence': historical,
    }


def _build_recommendation(business_type: str, metrics: dict[str, Any], historical: dict[str, Any], pattern: dict[str, Any]) -> dict[str, Any]:
    data_source = pattern.get('data_source') or _data_source([])
    if business_type == 'distributor':
        area = pattern.get('area')
        time_window = pattern.get('time_window')
        if not area or not time_window or pattern.get('delay_rate') is None:
            return {'status': 'insufficient_evidence', 'data_source': data_source}
        delivery_volume = pattern.get('delivery_volume') or 0
        delay_rate = float(pattern.get('delay_rate') or 0)
        duration = float(pattern.get('average_delivery_duration_minutes') or 0)
        recommendation = {
            'problem': f'{area} is experiencing recurring evening delivery delays.',
            'evidence': [
                f'{area} handled {delivery_volume} deliveries in the current operating window.',
                f'Average delivery duration was {duration:.0f} minutes with a {delay_rate * 100:.0f}% delay rate.',
                f'Peak congestion is concentrated during {time_window}.',
            ],
            'historical_evidence': historical.get('summary') or historical.get('message') or 'No historical memory was available for this operating pattern.',
            'proposed_action': f'Assign an additional delivery agent to {area} between {time_window} and advance dispatch timing for the next peak window.',
            'expected_impact': f'Reduce average delivery duration by roughly {max(10, min(20, int(duration * 0.35)))} minutes and lower the delay rate in the peak window.',
            'confidence': round(min(100, max(0, delay_rate * 100 + 50)), 2),
            'data_source': data_source,
        }
    else:
        area = pattern.get('area')
        if not area:
            return {'status': 'insufficient_evidence', 'data_source': data_source}
        recommendation = {
            'problem': f'Current operating evidence indicates a pressure point in {area}.',
            'evidence': metrics.get('evidence', ['Current operational evidence is available.']),
            'historical_evidence': historical.get('summary') or historical.get('message') or 'No historical memory was available.',
            'proposed_action': 'Rebalance capacity around the highest-demand operating window.',
            'expected_impact': 'Reduce strain in the busiest operating context without creating bottlenecks elsewhere.',
            'confidence': None,
            'data_source': data_source,
        }

    recommendation.update({
        'title': recommendation['problem'],
        'why': recommendation['problem'],
        'current_evidence': ' | '.join(recommendation['evidence']) if isinstance(recommendation['evidence'], list) else recommendation['evidence'],
        'historical_memory': recommendation['historical_evidence'],
        'expected_impact': recommendation['expected_impact'],
        'confidence': recommendation['confidence'],
    })
    return recommendation


def generate_intelligence(business_type: str, user_id: str, business_name: str = '') -> dict[str, Any]:
    records = get_business_records(business_type, user_id)
    if not records:
        return {
            'businessType': business_type,
            'businessName': business_name,
            'currentSignals': analyze_records(business_type, records),
            'detectedPattern': 'No operational records are available.',
            'currentEvidence': ['No operational records are available for this tenant.'],
            'historicalEvidence': {'status': 'not_available', 'message': 'No current evidence to match against historical memory.'},
            'insight': 'Import or connect operational records before requesting an AI recommendation.',
            'recommendation': None,
            'suggestedAction': None,
            'expectedImpact': None,
            'confidence': 0,
            'data_source': 'no_data',
            'synthetic': False,
        }
    metrics = analyze_records(business_type, records)
    pattern = _pattern_for_business(business_type, records, metrics)
    context = {
        'userId': user_id,
        'businessType': business_type,
        'businessName': business_name,
        'eventType': 'business_intelligence',
        'location': pattern.get('area'),
        'time_window': pattern.get('time_window'),
        'delivery_volume': pattern.get('delivery_volume'),
        'average_delivery_duration_minutes': pattern.get('average_delivery_duration_minutes'),
        'delay_rate': pattern.get('delay_rate'),
        'delivery_agent_workload': pattern.get('delivery_agent_workload'),
        'recurrence_across_dates': pattern.get('recurrence_across_dates'),
    }
    recalled = hindsight_service.recall_memory(context)
    historical_available = recalled.get('status') not in {'fallback', 'error'}
    historical = recalled if historical_available else {'status': 'fallback', 'message': 'Historical memory currently unavailable.'}
    facts = _recommendation_context(business_type, metrics, historical)
    llm_result = llm_service.generate_recommendation(facts)
    grounded_recommendation = _build_recommendation(business_type, metrics, historical, pattern)
    recommendation = None
    if llm_result:
        recommendation = {
            **grounded_recommendation,
            **{key: value for key, value in llm_result.items() if value is not None},
        }
    location = pattern.get('area') or facts['location']
    current_evidence = metrics.get('evidence', [])
    if recommendation:
        recommendation['data_source'] = pattern.get('data_source') or _data_source(records)
    return {
        'businessType': business_type,
        'businessName': business_name,
        'currentSignals': metrics,
        'detectedPattern': metrics.get('pattern'),
        'currentEvidence': current_evidence,
        'historicalEvidence': historical,
        'insight': metrics.get('insight'),
        'recommendation': recommendation,
        'suggestedAction': recommendation.get('proposed_action') or recommendation.get('title') if recommendation else None,
        'expectedImpact': recommendation.get('expected_impact') if recommendation else None,
        'confidence': recommendation.get('confidence', 0) if recommendation else 0,
        'data_source': pattern.get('data_source') or _data_source(records),
        'synthetic': False,
    }