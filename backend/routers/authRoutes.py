from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from core.auth import authenticate


router = APIRouter(prefix='/auth', tags=['auth'])


class AuthRequest(BaseModel):
	email: EmailStr
	password: str = Field(min_length=8)


@router.post('/login')
async def login(payload: AuthRequest):
	user = authenticate(str(payload.email), payload.password)
	if user is None:
		raise HTTPException(status_code=401, detail='Invalid email or password')
	return user
