from pydantic import BaseModel


class RestaurantOrder(BaseModel):
	order_id: str
	product: str
	location: str
	order_period: str
	sales: float
	demand: float
	customer_density: float
	foot_traffic: float
	coverage: float
