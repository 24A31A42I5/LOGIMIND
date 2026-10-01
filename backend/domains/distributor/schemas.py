from pydantic import BaseModel


class DistributorMetric(BaseModel):
	shipment_id: str
	customer: str
	location: str
	volume: float
	demand: float
	customer_density: float
	performance: float
	coverage: float
