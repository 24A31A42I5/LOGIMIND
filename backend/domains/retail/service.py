from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records


RETAIL_SALES = [
	{'sale_id': 'SALE-001', 'product': 'Home essentials', 'location': 'Area C', 'units': 94, 'demand': 84, 'customer_density': 88, 'purchasing_potential': 79, 'coverage': 36},
	{'sale_id': 'SALE-002', 'product': 'Personal care', 'location': 'Area C', 'units': 71, 'demand': 76, 'customer_density': 82, 'purchasing_potential': 75, 'coverage': 36},
	{'sale_id': 'SALE-003', 'product': 'Stationery', 'location': 'Area B', 'units': 42, 'demand': 54, 'customer_density': 60, 'purchasing_potential': 62, 'coverage': 81},
]


def list_sales(user_id: str | None = None) -> list[dict[str, Any]]:
	return read_domain_records('retail_sales', RETAIL_SALES, user_id)


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	return {'businessType': 'retail', 'currentData': normalize_metrics(list_sales(user_id)), 'hotspots': group_by_location(list_sales(user_id)), 'synthetic': not domain_records_are_persisted('retail_sales', user_id)}
