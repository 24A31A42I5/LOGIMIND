from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records


SUPPLY_ORDERS = [
	{'order_id': 'SUP-001', 'material': 'Steel coils', 'customer': 'Fabricator A', 'location': 'Industrial East', 'volume': 84, 'demand': 90, 'customer_density': 72, 'performance': 88, 'coverage': 48},
	{'order_id': 'SUP-002', 'material': 'Food-grade resin', 'customer': 'Packager B', 'location': 'Industrial East', 'volume': 61, 'demand': 77, 'customer_density': 68, 'performance': 91, 'coverage': 48},
	{'order_id': 'SUP-003', 'material': 'Aluminium', 'customer': 'Workshop C', 'location': 'Industrial North', 'volume': 43, 'demand': 58, 'customer_density': 55, 'performance': 83, 'coverage': 76},
]


def list_supplies(user_id: str | None = None) -> list[dict[str, Any]]:
	return read_domain_records('supplier_orders', SUPPLY_ORDERS, user_id)


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	return {'businessType': 'raw_material', 'currentData': normalize_metrics(list_supplies(user_id)), 'hotspots': group_by_location(list_supplies(user_id)), 'synthetic': not domain_records_are_persisted('supplier_orders', user_id)}
