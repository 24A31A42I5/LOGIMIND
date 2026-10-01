from fastapi import APIRouter, Depends, HTTPException, Query

from common.expansion.expansionService import get_expansion_analysis
from core.auth import get_current_user
from core.database import get_user_profile


router = APIRouter(prefix='/expansion', tags=['expansion'])


@router.get('')
async def expansion(business_type: str = Query(default='distributor'), current_user: dict = Depends(get_current_user)):
	try:
		profile = get_user_profile(current_user['userId'])
		return get_expansion_analysis(profile.get('businessType', 'distributor'), user_id=current_user['userId'])
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc
