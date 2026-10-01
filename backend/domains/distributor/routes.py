from fastapi import APIRouter, Depends

from core.auth import get_current_user
from common.repository import domain_records_are_persisted
from domains.distributor.service import get_metrics, list_operations


router = APIRouter(prefix='/distributor', tags=['distributor'])


@router.get('/operations')
async def operations(current_user: dict = Depends(get_current_user)):
	return {'businessType': 'distributor', 'records': list_operations(current_user['userId']), 'synthetic': not domain_records_are_persisted('distributor_shipments', current_user['userId'])}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	return get_metrics(current_user['userId'])
