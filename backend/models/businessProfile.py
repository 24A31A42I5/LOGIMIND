from typing import Literal

from pydantic import BaseModel, Field


BusinessType = Literal['distributor', 'restaurant', 'raw_material', 'retail', 'service_provider']


class Location(BaseModel):
	name: str = Field(min_length=1)
	latitude: float
	longitude: float


class BusinessProfile(BaseModel):
	userId: str = Field(min_length=1)
	businessType: BusinessType
	businessName: str = Field(min_length=1)
	locations: list[Location] = Field(default_factory=list)


class ProfileUpsert(BusinessProfile):
	pass
