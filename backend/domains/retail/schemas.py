from pydantic import BaseModel


class RetailSale(BaseModel):
	sale_id: str
	product: str
	location: str
	units: float
	demand: float
	customer_density: float
	purchasing_potential: float
	coverage: float
