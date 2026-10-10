from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from domains.raw_material.service import get_metrics, list_supplies
from common.repository import OperationalDataUnavailable


router = APIRouter(prefix='/raw-material', tags=['raw-material'])


@router.get('/supplies')
async def supplies(current_user: dict = Depends(get_current_user)):
	try:
		records = list_supplies(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
	return {'businessType': 'raw_material', 'records': records, 'data_source': 'mongodb', 'synthetic': False}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	try:
		return get_metrics(current_user['userId'])
	except OperationalDataUnavailable as exc:
		raise HTTPException(status_code=503, detail=str(exc)) from exc
