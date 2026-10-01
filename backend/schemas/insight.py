from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
	area: str = Field(min_length=1)


class InsightResponse(BaseModel):
	area: str
	current_evidence: str
	historical_evidence: str | None = None
	confidence: int | None = None
