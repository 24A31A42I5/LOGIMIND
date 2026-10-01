from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
	user_id: str = Field(min_length=1)
	email: EmailStr
	name: str | None = None
	active: bool = True
