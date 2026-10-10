from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from domains.restaurant.service import get_metrics, list_orders
from common.repository import OperationalDataUnavailable


router = APIRouter(prefix='/restaurant', tags=['restaurant'])


@router.get('/orders')
async def orders(current_user: dict = Depends(get_current_user)):
	try:
		records = list_orders(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
	return {'businessType': 'restaurant', 'records': records, 'data_source': 'mongodb', 'synthetic': False}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	try:
		return get_metrics(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
