from fastapi import APIRouter, Depends

from core.auth import get_current_user
from domains.retail.service import get_metrics, list_sales
from common.repository import domain_records_are_persisted


router = APIRouter(prefix='/retail', tags=['retail'])


@router.get('/sales')
async def sales(current_user: dict = Depends(get_current_user)):
	return {'businessType': 'retail', 'records': list_sales(current_user['userId']), 'synthetic': not domain_records_are_persisted('retail_sales', current_user['userId'])}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	return get_metrics(current_user['userId'])
