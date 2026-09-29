from fastapi import APIRouter, Query

from controllers.shipmentController import get_shipment_by_id, list_shipments

router = APIRouter(prefix='/shipments', tags=['shipments'])


@router.get('')
async def shipments(
    status: str | None = Query(default=None),
    area: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    shipment_id: str | None = Query(default=None),
):
    return await list_shipments(status=status, area=area, agent_id=agent_id, shipment_id=shipment_id)


@router.get('/{shipment_id}')
async def shipment_detail(shipment_id: str):
    return await get_shipment_by_id(shipment_id)
