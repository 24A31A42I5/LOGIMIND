from typing import Any

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
	user_id: str = Field(min_length=1)
	business_type: str = Field(min_length=1)
	recommendation: str = Field(min_length=1)
	why: str = Field(min_length=1)
	current_evidence: list[str] = Field(default_factory=list)
	historical_evidence: str = 'Historical memory unavailable.'
	expected_impact: str = Field(min_length=1)
	confidence: int = Field(ge=0, le=100)
	metadata: dict[str, Any] = Field(default_factory=dict)
