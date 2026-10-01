from dataclasses import dataclass


@dataclass
class SupplyOrder:
	order_id: str
	material: str
	customer: str
	area: str
	volume: float
	demand: float
	customer_density: float
	performance: float
	coverage: float
