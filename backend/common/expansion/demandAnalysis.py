from typing import Any, Iterable

from common.analytics.analyticsService import normalize_metrics


def assess_demand(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
	metrics = normalize_metrics(records)
	return {'demand': metrics['demand'], 'growth': metrics['growth'], 'trend': metrics['trend'], 'sufficientEvidence': metrics['volume'] > 0 or metrics['demand'] > 0}
