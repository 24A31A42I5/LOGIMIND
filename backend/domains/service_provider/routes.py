from fastapi import APIRouter, Depends

from core.auth import get_current_user
from domains.service_provider.service import get_metrics, list_bookings
from common.repository import domain_records_are_persisted


router = APIRouter(prefix='/service-provider', tags=['service-provider'])


@router.get('/bookings')
async def bookings(current_user: dict = Depends(get_current_user)):
	return {'businessType': 'service_provider', 'records': list_bookings(current_user['userId']), 'synthetic': not domain_records_are_persisted('service_bookings', current_user['userId'])}


@router.get('/metrics')
async def metrics(current_user: dict = Depends(get_current_user)):
	return get_metrics(current_user['userId'])
