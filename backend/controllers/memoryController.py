from services.hindsightService import hindsight_service
from services.seedService import get_demo_store


async def get_memory_recent():
    return get_demo_store()['memories']


async def recall_memory(query: str):
    memory = hindsight_service.recall_memory(query)
    if memory.get('status') == 'fallback':
        return {'historical_memory': 'Historical memory currently unavailable.', 'source': 'fallback'}
    return memory


async def reflect_memory(context: dict):
    memory = hindsight_service.reflect_memory(context)
    if memory.get('status') == 'fallback':
        return {'reflection': 'Historical memory currently unavailable.', 'source': 'fallback'}
    return memory


async def get_memory_stats():
    memories = get_demo_store()['memories']
    return {
        'total_memories': len(memories),
        'recent_patterns': [item['pattern'] for item in memories],
        'successful_interventions': 2,
        'unsuccessful_interventions': 1,
    }
