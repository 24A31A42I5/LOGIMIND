from pydantic import BaseModel, Field


class Location(BaseModel):
	name: str = Field(min_length=1)
	latitude: float = Field(ge=-90, le=90)
	longitude: float = Field(ge=-180, le=180)
	location_type: str = 'branch'
