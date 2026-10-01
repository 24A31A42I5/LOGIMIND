from dataclasses import dataclass


@dataclass
class RestaurantOrder:
	order_id: str
	product: str
	area: str
	order_period: str
	sales: float
	demand: float
	customer_density: float
	foot_traffic: float
	coverage: float
