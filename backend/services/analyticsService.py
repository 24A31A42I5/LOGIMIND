from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

from services.seedService import get_demo_store


def _percent(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def get_shipments() -> list[dict[str, Any]]:
    return sorted(get_demo_store()['shipments'], key=lambda item: item['dispatch_time'], reverse=True)


def get_delivery_agents() -> list[dict[str, Any]]:
    return get_demo_store()['delivery_agents']


def get_overall_analytics() -> dict[str, Any]:
    shipments = get_shipments()
    area_coordinates = {
        area['name']: (area['lat'], area['lng'])
        for area in get_demo_store().get('areas', [])
        if isinstance(area.get('lat'), (int, float)) and isinstance(area.get('lng'), (int, float))
    }
    total_deliveries = len(shipments)
    avg_duration = round(sum(item['duration_minutes'] for item in shipments) / total_deliveries, 2) if total_deliveries else 0
    delayed = sum(1 for item in shipments if item['status'] in {'Delayed', 'Failed'})
    failed = sum(1 for item in shipments if item['status'] == 'Failed')
    active_agents = len(get_delivery_agents())

    area_stats: dict[str, dict[str, Any]] = defaultdict(lambda: {'deliveries': 0, 'duration_total': 0, 'delayed': 0, 'failed': 0})
    for item in shipments:
        area = item['area']
        area_stats[area]['deliveries'] += 1
        area_stats[area]['duration_total'] += item['duration_minutes']
        if item['status'] in {'Delayed', 'Failed'}:
            area_stats[area]['delayed'] += 1
        if item['status'] == 'Failed':
            area_stats[area]['failed'] += 1

    hotspots = []
    for area, stats in area_stats.items():
        deliveries = stats['deliveries']
        avg_area = round(stats['duration_total'] / deliveries, 2) if deliveries else 0
        delay_rate = round(stats['delayed'] / deliveries, 4) if deliveries else 0
        hotspot = {
            'name': area,
            'lat': area_coordinates.get(area, (None, None))[0],
            'lng': area_coordinates.get(area, (None, None))[1],
            'deliveries': deliveries,
            'average_delivery_time': avg_area,
            'delay_rate': delay_rate,
            'reason': 'High delivery density + longer routes' if area == 'Area C' else 'Recurring route pressure',
            'peak_period': '6 PM – 8 PM' if area == 'Area C' else '4 PM – 7 PM',
            'performance': 'Hotspot' if area == 'Area C' else 'Stable',
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
        'peak_delivery_period': '6 PM – 8 PM',
        'recurring_patterns': ['Area C evening congestion', 'Weekend dispatch surge', 'Late-day route clustering'],
    }


def get_daily_analytics() -> dict[str, Any]:
    shipments = get_shipments()
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


def get_area_analytics() -> list[dict[str, Any]]:
    shipments = get_shipments()
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


def get_hotspots() -> list[dict[str, Any]]:
    return [{**item, 'type': 'hotspot' if item['delay_rate'] >= 20 else 'stable'} for item in get_overall_analytics()['area_hotspots']]


def get_trends() -> list[dict[str, Any]]:
    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for shipment in get_shipments():
        by_date[shipment['dispatch_time'][:10]].append(shipment)
    return [{'date': date, 'deliveries': len(items), 'avg_time': round(sum(item['duration_minutes'] for item in items) / len(items), 2)} for date, items in sorted(by_date.items())]


def get_monthly_analytics() -> dict[str, Any]:
    shipments = get_shipments()
    return {'month': datetime.now().strftime('%B %Y'), 'total_deliveries': len(shipments), 'average_delivery_time': round(sum(item['duration_minutes'] for item in shipments) / len(shipments), 2) if shipments else 0, 'delay_rate': _percent(sum(item['status'] in {'Delayed', 'Failed'} for item in shipments), len(shipments)), 'failed_delivery_rate': _percent(sum(item['status'] == 'Failed' for item in shipments), len(shipments))}
