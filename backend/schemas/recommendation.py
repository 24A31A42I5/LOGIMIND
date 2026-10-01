from pydantic import BaseModel


class Recommendation(BaseModel):
	recommendation: str
	why: str
	current_evidence: str
	historical_evidence: str | None = None
	expected_impact: str
	confidence: int | None = None