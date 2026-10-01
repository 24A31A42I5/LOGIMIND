from collections import defaultdict
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


def group_by_location(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
	groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
	for record in records:
		groups[record.get('location', 'Unknown')].append(record)
	return [{'location': location, **normalize_metrics(items)} for location, items in groups.items()]
