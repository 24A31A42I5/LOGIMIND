from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Iterable


def normalize_metrics(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
	records = list(records)
	if not records:
		return {
			'volume': 0,
			'demand': 0,
			'growth': 0,
			'customer_density': 0,
			'performance': None,
			'coverage': None,
			'trend': 'insufficient_evidence',
			'record_count': 0,
			'locations_count': 0,
			'data_status': 'no_data',
		}
	numeric = {key: [float(item[key]) for item in records if isinstance(item.get(key), (int, float))] for key in ('volume', 'demand', 'customer_density', 'performance', 'coverage')}
	result = {key: round(sum(values) / len(values), 2) if values else None for key, values in numeric.items()}
	result['growth'] = round(result['demand'] - result['volume'], 2) if result['demand'] is not None and result['volume'] is not None else None
	result['trend'] = 'growing' if result['growth'] is not None and result['growth'] > 0 else 'stable' if result['growth'] == 0 else 'insufficient_evidence'
	result['record_count'] = len(records)
	result['locations_count'] = len({item.get('location') or item.get('area') for item in records if item.get('location') or item.get('area')})
	result['data_status'] = 'observed'
	return result


def analyze_records(business_type: str, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
	records = list(records)
	base = normalize_metrics(records)
	base['domain_metrics'] = _domain_metrics(business_type, records)
	base['data_source'] = 'mongodb' if records else 'no_data'
	base['synthetic'] = False
	if not records:
		base['pattern'] = 'No operational records are available.'
		base['insight'] = 'Import operational records before requesting analysis.'
		base['evidence'] = ['No operational records are available for this tenant.']
		base.update({'businessType': business_type, 'hotspots': [], 'lowspots': [], 'peak_period': None})
		return base
	locations = group_by_location(records)
	for location in locations:
		coverage = location.get('coverage')
		location['coverage_gap'] = round(100 - coverage, 2) if coverage is not None else None
		coordinates = _location_coordinates(records, location['location'])
		location['coordinates'] = coordinates
		if coordinates:
			location['lat'] = coordinates['latitude']
			location['lng'] = coordinates['longitude']
	peak_periods = [record.get('order_period') or record.get('peak_period') for record in records]
	peak_period = max(set(filter(None, peak_periods)), key=peak_periods.count) if any(peak_periods) else 'observed operating hours'
	hotspots = sorted(locations, key=lambda item: (item.get('demand') is not None, item.get('demand') or 0, item.get('volume') or 0), reverse=True)
	lowspots = sorted(locations, key=lambda item: (item.get('demand') is None, item.get('demand') or 0, item.get('volume') or 0))
	base.update({
		'businessType': business_type,
		'volume': len(records) if not base['volume'] else base['volume'],
		'hotspots': hotspots,
		'lowspots': lowspots,
		'peak_period': peak_period,
		'growth': round(sum(record.get('demand', 0) for record in records) / len(records), 2) if records else 0,
		'data_source': 'mongodb',
		'synthetic': False,
	})
	base['pattern'] = f"Demand is concentrated in {base['hotspots'][0]['location']}" if base['hotspots'] else 'Insufficient evidence for a recurring pattern.'
	base['insight'] = f"{base['pattern']} during {peak_period}." if base['hotspots'] else 'More operating data is needed.'
	base['evidence'] = [
		f"{len(records)} current records across {len(locations)} locations.",
		f"Top location: {base['hotspots'][0]['location']} with demand {base['hotspots'][0].get('demand', 0)}." if base['hotspots'] else 'No location evidence available.',
		f"Peak period: {peak_period}.",
	]
	return base


def _number(record: dict[str, Any], *keys: str) -> float | None:
	for key in keys:
		value = record.get(key)
		if isinstance(value, (int, float)):
			return float(value)
	return None


def _average(values: list[float]) -> float | None:
	return round(sum(values) / len(values), 2) if values else None


def _domain_metrics(business_type: str, records: list[dict[str, Any]]) -> dict[str, Any]:
	if not records:
		return {}
	if business_type == 'restaurant':
		revenue = [_number(item, 'sales', 'revenue', 'amount') for item in records]
		prep = [_number(item, 'prep_time_minutes', 'preparation_time', 'order_preparation_minutes') for item in records]
		cost = [_number(item, 'food_cost', 'cost') for item in records]
		revenue_values = [value for value in revenue if value is not None]
		cost_values = [value for value in cost if value is not None]
		return {
			'orders': len(records),
			'revenue': round(sum(revenue_values), 2) if revenue_values else None,
			'average_order_value': _average(revenue_values),
			'average_preparation_minutes': _average([value for value in prep if value is not None]),
			'food_cost_percentage': round(sum(cost_values) / sum(revenue_values) * 100, 2) if cost_values and sum(revenue_values) else None,
		}
	if business_type == 'retail':
		revenue = [_number(item, 'sales', 'revenue', 'amount') for item in records]
		margin = [_number(item, 'margin', 'gross_margin') for item in records]
		units = [_number(item, 'units', 'quantity') for item in records]
		revenue_values = [value for value in revenue if value is not None]
		margin_values = [value for value in margin if value is not None]
		return {
			'transactions': len(records),
			'revenue': round(sum(revenue_values), 2) if revenue_values else None,
			'units_sold': round(sum(value for value in units if value is not None), 2) if any(value is not None for value in units) else None,
			'gross_margin_percentage': round(sum(margin_values) / sum(revenue_values) * 100, 2) if margin_values and sum(revenue_values) else None,
			'stockouts': sum(1 for item in records if str(item.get('status', '')).lower() in {'stockout', 'out_of_stock'}),
		}
	if business_type == 'raw_material':
		lead_times = [_number(item, 'lead_time_days', 'lead_time') for item in records]
		return {
			'open_orders': sum(1 for item in records if str(item.get('status', '')).lower() in {'open', 'pending', 'in_progress'}),
			'available_stock': sum(value for value in (_number(item, 'stock', 'available_stock', 'quantity', 'volume') for item in records) if value is not None),
			'average_lead_time_days': _average([value for value in lead_times if value is not None]),
			'supplier_on_time_rate': _rate(records, {'on_time', 'delivered_on_time', 'completed_on_time'}),
		}
	if business_type == 'service_provider':
		resolution = [_number(item, 'resolution_time_hours', 'resolution_hours', 'duration_hours') for item in records]
		return {
			'open_work_orders': sum(1 for item in records if str(item.get('status', '')).lower() in {'open', 'pending', 'assigned', 'in_progress'}),
			'completed_work_orders': sum(1 for item in records if str(item.get('status', '')).lower() in {'completed', 'closed', 'resolved'}),
			'average_resolution_hours': _average([value for value in resolution if value is not None]),
			'sla_compliance_rate': _rate(records, {'sla_met', 'within_sla', 'on_time'}),
		}
	return {}


def _rate(records: list[dict[str, Any]], true_values: set[str]) -> float | None:
	observed = [
		item.get('on_time', item.get('sla_met', item.get('within_sla')))
		for item in records
		if item.get('on_time') is not None or item.get('sla_met') is not None or item.get('within_sla') is not None
	]
	if not observed:
		return None
	return round(sum(1 for value in observed if value is True or str(value).lower() in true_values) / len(observed) * 100, 2)


def group_by_location(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
	groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
	for record in records:
		location = record.get('location') or record.get('area') or record.get('region')
		if location:
			groups[str(location)].append(record)
	return [{'location': location, **normalize_metrics(items)} for location, items in groups.items()]


def _location_coordinates(records: list[dict[str, Any]], location: str) -> dict[str, float] | None:
	points = [
		(record.get('latitude', record.get('lat')), record.get('longitude', record.get('lng')))
		for record in records
		if record.get('location', 'Unknown') == location
	]
	valid = [(float(latitude), float(longitude)) for latitude, longitude in points if latitude is not None and longitude is not None]
	if not valid:
		return None
	return {
		'latitude': round(sum(point[0] for point in valid) / len(valid), 6),
		'longitude': round(sum(point[1] for point in valid) / len(valid), 6),
	}


def filter_records_by_period(records: Iterable[dict[str, Any]], period: str = 'overall', now: datetime | None = None) -> list[dict[str, Any]]:
	if period == 'overall':
		return list(records)
	now = now or datetime.now()
	days = {'today': 1, 'week': 7, 'month': 30}.get(period)
	if days is None:
		return list(records)
	start = now - timedelta(days=days - 1)
	filtered = []
	for record in records:
		value = record.get('timestamp') or record.get('date') or record.get('dispatch_time') or record.get('purchase_date')
		try:
			date_value = datetime.fromisoformat(str(value).replace('Z', '+00:00')).replace(tzinfo=None)
		except (TypeError, ValueError):
			continue
		if date_value >= start:
			filtered.append(record)
	return filtered
