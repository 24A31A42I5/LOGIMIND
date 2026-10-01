from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records
from services.seedService import get_demo_store


def list_operations(user_id: str | None = None) -> list[dict[str, Any]]:
	seed_records = [
		{'shipment_id': item['shipment_id'], 'customer': item['customer'], 'location': item['area'], 'volume': 1, 'demand': 1, 'customer_density': 330 if item['area'] == 'Area C' else 220, 'performance': max(0, 100 - item['delay_minutes']), 'coverage': 70 if item['area'] == 'Area C' else 90}
		for item in get_demo_store()['shipments'][:60]
	]
	return read_domain_records('distributor_shipments', seed_records, user_id)


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	records = list_operations(user_id)
	return {'businessType': 'distributor', 'currentData': normalize_metrics(records), 'hotspots': group_by_location(records), 'synthetic': not domain_records_are_persisted('distributor_shipments', user_id)}
