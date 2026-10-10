from fastapi import HTTPException

from services.analyticsService import get_delivery_agents


async def list_agents(user: dict):
    return get_delivery_agents(user['userId'])


async def get_agent_by_id(agent_id: str, user: dict):
    for agent in get_delivery_agents(user['userId']):
        if agent['agent_id'] == agent_id:
            return agent
    raise HTTPException(status_code=404, detail='Delivery agent not found')
