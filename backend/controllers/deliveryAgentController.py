from services.analyticsService import get_delivery_agents


async def list_agents():
    return get_delivery_agents()


async def get_agent_by_id(agent_id: str):
    for agent in get_delivery_agents():
        if agent['agent_id'] == agent_id:
            return agent
    return {'detail': 'Agent not found'}
