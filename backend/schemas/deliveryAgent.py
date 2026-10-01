from pydantic import BaseModel


class DeliveryAgent(BaseModel):
	agent_id: str
	status: str
	region: str
	today_deliveries: int = 0
	completed: int = 0
	delayed: int = 0
	failed: int = 0
