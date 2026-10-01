from pydantic import BaseModel


class Shipment(BaseModel):
	shipment_id: str
	product: str
	customer: str
	destination: str
	area: str
	agent_id: str
	status: str
	duration_minutes: int = 0
	distance_km: int = 0
