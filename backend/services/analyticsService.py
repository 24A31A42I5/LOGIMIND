from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

from common.ai.intelligenceService import get_business_records
from common.analytics.analyticsService import filter_records_by_period
from common.repository import read_domain_records, update_domain_record


def _agent_location(agent: dict[str, Any]) -> dict[str, Any] | None:
	location = agent.get('last_location')
	if not isinstance(location, dict):
		location = agent.get('location') if isinstance(agent.get('location'), dict) else agent
	latitude = location.get('latitude', location.get('lat'))
	longitude = location.get('longitude', location.get('lng', location.get('lon')))
	if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
		return None
	if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
		return None
	return {
		'agent_id': agent.get('agent_id'),
		'latitude': latitude,
		'longitude': longitude,
		'recorded_at': location.get('recorded_at', agent.get('location_updated_at')),
		'status': agent.get('status'),
		'region': agent.get('region'),
	}


def _percent(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def get_shipments(user_id: str) -> list[dict[str, Any]]:
    return sorted(get_business_records('distributor', user_id), key=lambda item: item.get('dispatch_time', ''), reverse=True)


def get_delivery_agents(user_id: str) -> list[dict[str, Any]]:
    return read_domain_records('delivery_agents', user_id)


def get_agent_locations(user_id: str) -> list[dict[str, Any]]:
    return [
        location
        for agent in get_delivery_agents(user_id)
        if (location := _agent_location(agent)) is not None
    ]


def update_agent_location(
    user_id: str,
    agent_id: str,
    latitude: float,
    longitude: float,
    recorded_at: str,
) -> dict[str, Any]:
    location = {
        'latitude': latitude,
        'longitude': longitude,
        'recorded_at': recorded_at,
    }
    updated = update_domain_record(
        'delivery_agents',
        {'userId': user_id, 'agent_id': agent_id},
        {'last_location': location, 'location_updated_at': recorded_at},
    )
    if not updated:
        raise KeyError(agent_id)
    return {'agent_id': agent_id, **location}


def get_overall_analytics(business_type: str = 'distributor', user_id: str | None = None, period: str = 'overall') -> dict[str, Any]:
    if business_type != 'distributor':
        from common.analytics.analyticsService import analyze_records
        return analyze_records(business_type, filter_records_by_period(get_business_records(business_type, user_id or ''), period))
    shipments = filter_records_by_period(get_shipments(user_id), period)
    total_deliveries = len(shipments)
    avg_duration = round(sum(item['duration_minutes'] for item in shipments) / total_deliveries, 2) if total_deliveries else 0
    delayed = sum(1 for item in shipments if item['status'] in {'Delayed', 'Failed'})
    failed = sum(1 for item in shipments if item['status'] == 'Failed')
    active_agents = len(get_delivery_agents(user_id))

    area_stats: dict[str, dict[str, Any]] = defaultdict(lambda: {'deliveries': 0, 'duration_total': 0, 'delayed': 0, 'failed': 0, 'latitudes': [], 'longitudes': []})
    for item in shipments:
        area = item['area']
        area_stats[area]['deliveries'] += 1
        area_stats[area]['duration_total'] += item['duration_minutes']
        if item['status'] in {'Delayed', 'Failed'}:
            area_stats[area]['delayed'] += 1
        if item['status'] == 'Failed':
            area_stats[area]['failed'] += 1
        if isinstance(item.get('customer_lat'), (int, float)) and isinstance(item.get('customer_lng'), (int, float)):
            area_stats[area]['latitudes'].append(item['customer_lat'])
            area_stats[area]['longitudes'].append(item['customer_lng'])

    hotspots = []
    for area, stats in area_stats.items():
        deliveries = stats['deliveries']
        avg_area = round(stats['duration_total'] / deliveries, 2) if deliveries else 0
        delay_rate = round(stats['delayed'] / deliveries, 4) if deliveries else 0
        hotspot = {
            'name': area,
            'lat': round(sum(stats['latitudes']) / len(stats['latitudes']), 6) if stats['latitudes'] else None,
            'lng': round(sum(stats['longitudes']) / len(stats['longitudes']), 6) if stats['longitudes'] else None,
            'deliveries': deliveries,
            'average_delivery_time': avg_area,
            'delay_rate': delay_rate,
            'reason': 'Higher observed delivery volume and delay rate' if delay_rate > 0 else 'Observed delivery activity',
            'performance': 'Hotspot' if delay_rate * 100 >= 20 else 'Observed',
        }
        hotspots.append(hotspot)

    hotspots = sorted(hotspots, key=lambda item: item['deliveries'], reverse=True)
    return {
        'total_deliveries': total_deliveries,
        'average_delivery_time': avg_duration,
        'delay_rate': _percent(delayed, total_deliveries),
        'failed_delivery_rate': _percent(failed, total_deliveries),
        'active_agents': active_agents,
        'area_hotspots': hotspots,
        'peak_delivery_period': _peak_delivery_period(shipments),
        'recurring_patterns': _delivery_patterns(shipments),
        'data_source': 'mongodb' if shipments else 'no_data',
        'synthetic': False,
    }


def _peak_delivery_period(shipments: list[dict[str, Any]]) -> str:
    hours = []
    for item in shipments:
        try:
            hours.append(datetime.fromisoformat(item['dispatch_time']).hour)
        except (KeyError, TypeError, ValueError):
            continue
    if not hours:
        return 'insufficient evidence'
    start = min(hours)
    end = max(hours) + 1
    return f'{start:02d}:00-{end:02d}:00'


def _delivery_patterns(shipments: list[dict[str, Any]]) -> list[str]:
    patterns = []
    delayed = sum(item.get('status') in {'Delayed', 'Failed'} for item in shipments)
    if delayed and delayed / len(shipments) >= 0.2:
        patterns.append('elevated delay rate')
    if len({item.get('area') for item in shipments}) > 1:
        patterns.append('multi-location delivery activity')
    return patterns or ['insufficient evidence for a recurring pattern']


def get_daily_analytics(business_type: str = 'distributor', user_id: str | None = None) -> dict[str, Any]:
    if business_type != 'distributor':
        from common.analytics.analyticsService import analyze_records
        return analyze_records(business_type, get_business_records(business_type, user_id or ''))
    shipments = get_shipments(user_id)
    by_hour: dict[str, int] = defaultdict(int)
    for item in shipments:
        dt = datetime.fromisoformat(item['dispatch_time'])
        by_hour[str(dt.hour)] += 1

    return {
        'today': 'Today',
        'timeline': [{'time': hour, 'deliveries': value} for hour, value in sorted(by_hour.items(), key=lambda x: int(x[0]))],
        'average_delivery_time': round(sum(item['duration_minutes'] for item in shipments) / len(shipments), 2) if shipments else 0,
        'delayed_shipments': sum(1 for item in shipments if item['status'] in {'Delayed', 'Failed'}),
    }


def get_area_analytics(business_type: str = 'distributor', user_id: str | None = None) -> list[dict[str, Any]]:
    if business_type != 'distributor':
        return get_overall_analytics(business_type, user_id).get('hotspots', [])
    shipments = get_shipments(user_id)
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {'deliveries': 0, 'time_total': 0, 'delay_total': 0})
    for item in shipments:
        area = item['area']
        stats[area]['deliveries'] += 1
        stats[area]['time_total'] += item['duration_minutes']
        if item['status'] in {'Delayed', 'Failed'}:
            stats[area]['delay_total'] += 1
    result = []
    for area, values in stats.items():
        deliveries = values['deliveries']
        result.append({
            'area': area,
            'deliveries': deliveries,
            'average_delivery_time': round(values['time_total'] / deliveries, 2) if deliveries else 0,
            'delay_rate': _percent(values['delay_total'], deliveries),
        })
    return sorted(result, key=lambda item: item['deliveries'], reverse=True)


def get_hotspots(business_type: str = 'distributor', user_id: str | None = None) -> list[dict[str, Any]]:
    items = get_overall_analytics(business_type, user_id).get('area_hotspots', get_overall_analytics(business_type, user_id).get('hotspots', []))
    return [{**item, 'type': 'hotspot' if item.get('delay_rate', item.get('coverage_gap', 0)) >= 20 else 'stable'} for item in items]


def get_trends(business_type: str = 'distributor', user_id: str | None = None) -> list[dict[str, Any]]:
    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in get_business_records(business_type, user_id or ''):
        date = record.get('timestamp', record.get('dispatch_time', ''))[:10]
        by_date[date].append(record)
    return [{'date': date, 'volume': len(items), 'demand': round(sum(item.get('demand', item.get('duration_minutes', 0)) for item in items) / len(items), 2)} for date, items in sorted(by_date.items())]


def get_monthly_analytics(business_type: str = 'distributor', user_id: str | None = None) -> dict[str, Any]:
    if business_type != 'distributor':
        from common.analytics.analyticsService import analyze_records
        metrics = analyze_records(business_type, get_business_records(business_type, user_id or ''))
        return {'businessType': business_type, 'currentData': metrics, 'synthetic': False, 'data_source': 'mongodb'}
    shipments = get_shipments(user_id)
    return {'month': datetime.now().strftime('%B %Y'), 'total_deliveries': len(shipments), 'average_delivery_time': round(sum(item['duration_minutes'] for item in shipments) / len(shipments), 2) if shipments else 0, 'delay_rate': _percent(sum(item['status'] in {'Delayed', 'Failed'} for item in shipments), len(shipments)), 'failed_delivery_rate': _percent(sum(item['status'] == 'Failed' for item in shipments), len(shipments))}
