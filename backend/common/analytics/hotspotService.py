from typing import Any, Iterable

from common.analytics.analyticsService import group_by_location


def detect_hotspots(records: Iterable[dict[str, Any]], minimum_demand: float = 0) -> list[dict[str, Any]]:
	locations = group_by_location(records)
	return sorted([location for location in locations if location['demand'] >= minimum_demand], key=lambda item: (item['demand'], item['customer_density']), reverse=True)
