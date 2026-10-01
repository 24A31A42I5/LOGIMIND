from pydantic import BaseModel


class ServiceBooking(BaseModel):
	booking_id: str
	service: str
	location: str
	demand: float
	customer_density: float
	competition: float
	operational_feasibility: float
	coverage: float
