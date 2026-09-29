from fastapi import APIRouter

from controllers.deliveryAgentController import get_agent_by_id, list_agents

router = APIRouter(prefix='/delivery-agents', tags=['delivery-agents'])


@router.get('')
async def delivery_agents():
    return await list_agents()


@router.get('/{agent_id}')
async def delivery_agent_detail(agent_id: str):
    return await get_agent_by_id(agent_id)
