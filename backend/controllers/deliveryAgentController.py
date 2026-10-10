from fastapi import HTTPException

from services.analyticsService import (
    get_agent_locations,
    get_delivery_agents,
    update_agent_location,
)


async def list_agents(user: dict):
    return get_delivery_agents(user['userId'])


async def list_agent_locations(user: dict):
    return {
        'locations': get_agent_locations(user['userId']),
        'data_source': 'mongodb',
        'synthetic': False,
    }


async def get_agent_by_id(agent_id: str, user: dict):
    for agent in get_delivery_agents(user['userId']):
        if agent['agent_id'] == agent_id:
            return agent
    raise HTTPException(status_code=404, detail='Delivery agent not found')


async def save_agent_location(agent_id: str, payload, user: dict):
    try:
        return update_agent_location(
            user['userId'],
            agent_id,
            payload.latitude,
            payload.longitude,
            payload.recorded_at.isoformat(),
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail='Delivery agent not found') from exc
