from typing import Any

from common.analytics.analyticsService import group_by_location, normalize_metrics
from common.repository import domain_records_are_persisted, read_domain_records


SERVICE_BOOKINGS = [
	{'booking_id': 'BOOK-001', 'service': 'Home maintenance', 'location': 'Area C', 'demand': 89, 'customer_density': 84, 'competition': 42, 'operational_feasibility': 78, 'coverage': 31},
	{'booking_id': 'BOOK-002', 'service': 'Home maintenance', 'location': 'Area C', 'demand': 81, 'customer_density': 79, 'competition': 42, 'operational_feasibility': 76, 'coverage': 31},
	{'booking_id': 'BOOK-003', 'service': 'Appliance repair', 'location': 'Area D', 'demand': 63, 'customer_density': 65, 'competition': 34, 'operational_feasibility': 61, 'coverage': 69},
]


def list_bookings(user_id: str | None = None) -> list[dict[str, Any]]:
	return read_domain_records('service_bookings', SERVICE_BOOKINGS, user_id)


def get_metrics(user_id: str | None = None) -> dict[str, Any]:
	return {'businessType': 'service_provider', 'currentData': normalize_metrics(list_bookings(user_id)), 'hotspots': group_by_location(list_bookings(user_id)), 'synthetic': not domain_records_are_persisted('service_bookings', user_id)}
