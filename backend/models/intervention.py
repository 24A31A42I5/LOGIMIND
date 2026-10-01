from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Intervention(BaseModel):
	user_id: str = Field(min_length=1)
	business_type: str = Field(min_length=1)
	title: str = Field(min_length=1)
	action: str = Field(min_length=1)
	area: str = Field(min_length=1)
	outcome: str | None = None
	created_at: datetime | None = None
	metadata: dict[str, Any] = Field(default_factory=dict)
