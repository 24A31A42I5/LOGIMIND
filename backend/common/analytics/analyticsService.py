from collections import defaultdict
from datetime import datetime
from typing import Any, Iterable


def normalize_metrics(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
	records = list(records)
	if not records:
		return {'volume': 0, 'demand': 0, 'growth': 0, 'customer_density': 0, 'performance': 0, 'coverage': 0, 'trend': 'insufficient_evidence'}
	numeric = {key: [float(item[key]) for item in records if isinstance(item.get(key), (int, float))] for key in ('volume', 'demand', 'customer_density', 'performance', 'coverage')}
	result = {key: round(sum(values) / len(values), 2) if values else 0 for key, values in numeric.items()}
	result['growth'] = round(result['demand'] - result['volume'], 2)
	result['trend'] = 'growing' if result['growth'] > 0 else 'stable' if result['growth'] == 0 else 'declining'
	return result


def analyze_records(business_type: str, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
	records = list(records)
	base = normalize_metrics(records)
	locations = group_by_location(records)
	for location in locations:
		location['coverage_gap'] = round(100 - location.get('coverage', 0), 2)
	peak_periods = [record.get('order_period') or record.get('peak_period') for record in records]
	peak_period = max(set(peak_periods), key=peak_periods.count) if any(peak_periods) else 'observed operating hours'
	base.update({
		'businessType': business_type,
		'volume': len(records) if not base['volume'] else base['volume'],
		'hotspots': sorted(locations, key=lambda item: (item.get('demand', 0), item.get('coverage_gap', 0)), reverse=True),
		'peak_period': peak_period,
		'growth': round(sum(record.get('demand', 0) for record in records) / len(records), 2) if records else 0,
	})
	base['pattern'] = f"Demand is concentrated in {base['hotspots'][0]['location']}" if base['hotspots'] else 'Insufficient evidence for a recurring pattern.'
	base['insight'] = f"{base['pattern']} during {peak_period}." if base['hotspots'] else 'More operating data is needed.'
	base['evidence'] = [
		f"{len(records)} current records across {len(locations)} locations.",
		f"Top location: {base['hotspots'][0]['location']} with demand {base['hotspots'][0].get('demand', 0)}." if base['hotspots'] else 'No location evidence available.',
		f"Peak period: {peak_period}.",
	]
	return base


def group_by_location(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
	groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
	for record in records:
		groups[record.get('location', 'Unknown')].append(record)
	return [{'location': location, **normalize_metrics(items)} for location, items in groups.items()]
