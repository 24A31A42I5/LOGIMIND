from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records


def list_supplies(user_id: str | None = None) -> list[dict[str, Any]]:
	return read_domain_records('supplier_orders', user_id or '')


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	records = list_supplies(user_id)
	return {'businessType': 'raw_material', 'currentData': normalize_metrics(records), 'hotspots': group_by_location(records), 'synthetic': False, 'data_source': 'mongodb'}
