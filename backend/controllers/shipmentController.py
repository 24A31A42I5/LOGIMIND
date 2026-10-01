from fastapi import HTTPException

from services.analyticsService import get_shipments


async def list_shipments(status: str | None = None, area: str | None = None, agent_id: str | None = None, shipment_id: str | None = None):
    shipments = get_shipments()
    if status:
        shipments = [item for item in shipments if item['status'].lower() == status.lower()]
    if area:
        shipments = [item for item in shipments if item['area'].lower() == area.lower()]
    if agent_id:
        shipments = [item for item in shipments if item['agent_id'].lower() == agent_id.lower()]
    if shipment_id:
        shipments = [item for item in shipments if item['shipment_id'].lower() == shipment_id.lower()]
    return shipments


async def get_shipment_by_id(shipment_id: str):
    shipments = get_shipments()
    for shipment in shipments:
        if shipment['shipment_id'] == shipment_id:
            return shipment
        raise HTTPException(status_code=404, detail='Shipment not found')
