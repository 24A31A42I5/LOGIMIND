from fastapi import APIRouter, Depends

from core.auth import get_current_user
from domains.raw_material.service import get_metrics, list_supplies
from common.repository import domain_records_are_persisted


router = APIRouter(prefix='/raw-material', tags=['raw-material'])


@router.get('/supplies')
async def supplies(current_user: dict = Depends(get_current_user)):
	return {'businessType': 'raw_material', 'records': list_supplies(current_user['userId']), 'synthetic': not domain_records_are_persisted('supplier_orders', current_user['userId'])}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	return get_metrics(current_user['userId'])
