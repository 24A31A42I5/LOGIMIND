from fastapi import APIRouter, Depends

from controllers.deliveryAgentController import (
    get_agent_by_id,
    list_agent_locations,
    list_agents,
    save_agent_location,
)
from core.auth import get_current_user
from schemas.agentLocation import AgentLocationUpdate

router = APIRouter(prefix='/delivery-agents', tags=['delivery-agents'])


@router.get('')
async def delivery_agents(current_user: dict = Depends(get_current_user)):
    return await list_agents(current_user)


@router.get('/locations')
async def delivery_agent_locations(current_user: dict = Depends(get_current_user)):
    return await list_agent_locations(current_user)


@router.post('/{agent_id}/location')
async def update_delivery_agent_location(
    agent_id: str,
    payload: AgentLocationUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await save_agent_location(agent_id, payload, current_user)


@router.get('/{agent_id}')
async def delivery_agent_detail(agent_id: str, current_user: dict = Depends(get_current_user)):
    return await get_agent_by_id(agent_id, current_user)
