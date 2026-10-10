from fastapi import APIRouter, Depends

from controllers.deliveryAgentController import get_agent_by_id, list_agents
from core.auth import get_current_user

router = APIRouter(prefix='/delivery-agents', tags=['delivery-agents'])


@router.get('')
async def delivery_agents(current_user: dict = Depends(get_current_user)):
    return await list_agents(current_user)


@router.get('/{agent_id}')
async def delivery_agent_detail(agent_id: str, current_user: dict = Depends(get_current_user)):
    return await get_agent_by_id(agent_id, current_user)
