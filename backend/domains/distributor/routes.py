from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from common.repository import OperationalDataUnavailable, domain_records_are_persisted
from domains.distributor.service import get_metrics, list_operations


router = APIRouter(prefix='/distributor', tags=['distributor'])


@router.get('/operations')
async def operations(current_user: dict = Depends(get_current_user)):
	try:
		records = list_operations(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
	return {'businessType': 'distributor', 'records': records, 'data_source': 'mongodb', 'synthetic': False}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	try:
		return get_metrics(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
