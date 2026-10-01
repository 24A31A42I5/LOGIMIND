from dataclasses import dataclass


@dataclass
class DistributorOperation:
	shipment_id: str
	customer: str
	area: str
	status: str
	volume: float
	demand: float
	customer_density: float
	performance: float
	coverage: float
