from dataclasses import dataclass


@dataclass
class ServiceBooking:
	booking_id: str
	service: str
	area: str
	demand: float
	customer_density: float
	competition: float
	operational_feasibility: float
	coverage: float
