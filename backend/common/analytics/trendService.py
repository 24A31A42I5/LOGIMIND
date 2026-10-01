from typing import Any, Iterable


def calculate_trend(records: Iterable[dict[str, Any]], value_key: str = 'demand') -> dict[str, Any]:
	values = [float(record[value_key]) for record in records if isinstance(record.get(value_key), (int, float))]
	if len(values) < 2:
		return {'direction': 'insufficient_evidence', 'change': 0, 'observations': len(values)}
	change = round(values[-1] - values[0], 2)
	return {'direction': 'growing' if change > 0 else 'declining' if change < 0 else 'stable', 'change': change, 'observations': len(values)}
