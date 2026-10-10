from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from domains.service_provider.service import get_metrics, list_bookings
from common.repository import OperationalDataUnavailable


router = APIRouter(prefix='/service-provider', tags=['service-provider'])


@router.get('/bookings')
async def bookings(current_user: dict = Depends(get_current_user)):
	try:
		records = list_bookings(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
	return {'businessType': 'service_provider', 'records': records, 'data_source': 'mongodb', 'synthetic': False}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	try:
		return get_metrics(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
