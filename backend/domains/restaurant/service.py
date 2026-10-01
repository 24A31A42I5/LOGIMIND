from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records


RESTAURANT_ORDERS = [
	{'order_id': 'ORD-001', 'product': 'Thali', 'location': 'Area C', 'order_period': '18:00-21:00', 'sales': 4200, 'demand': 92, 'customer_density': 86, 'foot_traffic': 88, 'coverage': 42},
	{'order_id': 'ORD-002', 'product': 'Biryani', 'location': 'Area C', 'order_period': '18:00-21:00', 'sales': 3600, 'demand': 88, 'customer_density': 81, 'foot_traffic': 84, 'coverage': 42},
	{'order_id': 'ORD-003', 'product': 'Breakfast', 'location': 'Area A', 'order_period': '07:00-10:00', 'sales': 2400, 'demand': 64, 'customer_density': 62, 'foot_traffic': 69, 'coverage': 78},
]


def list_orders(user_id: str | None = None) -> list[dict[str, Any]]:
	return read_domain_records('restaurant_orders', RESTAURANT_ORDERS, user_id)


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	return {'businessType': 'restaurant', 'currentData': normalize_metrics(list_orders(user_id)), 'hotspots': group_by_location(list_orders(user_id)), 'synthetic': not domain_records_are_persisted('restaurant_orders', user_id)}
