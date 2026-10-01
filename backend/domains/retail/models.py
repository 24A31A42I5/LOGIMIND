from dataclasses import dataclass


@dataclass
class RetailSale:
	sale_id: str
	product: str
	area: str
	units: float
	demand: float
	customer_density: float
	purchasing_potential: float
	coverage: float
