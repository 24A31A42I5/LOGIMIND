from pydantic import BaseModel


class SupplyOrder(BaseModel):
	order_id: str
	material: str
	customer: str
	location: str
	volume: float
	demand: float
	customer_density: float
	performance: float
	coverage: float
