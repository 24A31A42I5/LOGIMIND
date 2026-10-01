from fastapi import APIRouter, Depends

from core.auth import get_current_user
from domains.restaurant.service import get_metrics, list_orders
from common.repository import domain_records_are_persisted


router = APIRouter(prefix='/restaurant', tags=['restaurant'])


@router.get('/orders')
async def orders(current_user: dict = Depends(get_current_user)):
	return {'businessType': 'restaurant', 'records': list_orders(current_user['userId']), 'synthetic': not domain_records_are_persisted('restaurant_orders', current_user['userId'])}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	return get_metrics(current_user['userId'])
