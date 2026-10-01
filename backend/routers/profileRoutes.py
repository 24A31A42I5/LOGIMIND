from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from core.database import get_fallback_profile, get_profiles_collection, save_fallback_profile
from models.businessProfile import BusinessProfile, ProfileUpsert


router = APIRouter(prefix='/profile', tags=['profile'])


@router.get('/{user_id}', response_model=BusinessProfile)
async def get_profile(user_id: str, current_user: dict = Depends(get_current_user)):
	if current_user['userId'] != user_id:
		raise HTTPException(status_code=403, detail='Profile access denied')
	collection = get_profiles_collection()
	if collection is not None:
		try:
			profile = collection.find_one({'userId': user_id}, {'_id': 0})
		except Exception as exc:
			raise HTTPException(status_code=503, detail='MongoDB profile lookup failed') from exc
	else:
		profile = get_fallback_profile(user_id)
	if profile is None:
		raise HTTPException(status_code=404, detail='Business profile not found')
	return profile


@router.put('', response_model=BusinessProfile)
async def upsert_profile(payload: ProfileUpsert, current_user: dict = Depends(get_current_user)):
	if current_user['userId'] != payload.userId:
		raise HTTPException(status_code=403, detail='Profile ownership mismatch')
	profile = payload.model_dump()
	collection = get_profiles_collection()
	if collection is not None:
		try:
			collection.replace_one({'userId': profile['userId']}, profile, upsert=True)
		except Exception as exc:
			raise HTTPException(status_code=503, detail='MongoDB profile save failed') from exc
	else:
		save_fallback_profile(profile)
	return profile
