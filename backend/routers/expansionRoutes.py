from fastapi import APIRouter, Depends, HTTPException, Query

from common.expansion.expansionService import get_expansion_analysis
from core.auth import get_current_user


router = APIRouter(prefix='/expansion', tags=['expansion'])


@router.get('')
async def expansion(business_type: str = Query(default='distributor'), current_user: dict = Depends(get_current_user)):
	try:
		return get_expansion_analysis(business_type, user_id=current_user['userId'])
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc
