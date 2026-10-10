from fastapi import APIRouter, Depends, Query

from controllers.shipmentController import get_shipment_by_id, list_shipments
from core.auth import get_current_user

router = APIRouter(prefix='/shipments', tags=['shipments'])


@router.get('')
async def shipments(
    status: str | None = Query(default=None),
    area: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    shipment_id: str | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    return await list_shipments(current_user, status=status, area=area, agent_id=agent_id, shipment_id=shipment_id)


@router.get('/{shipment_id}')
async def shipment_detail(shipment_id: str, current_user: dict = Depends(get_current_user)):
    return await get_shipment_by_id(shipment_id, current_user)
