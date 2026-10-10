from core.database import get_user_profile
from services.hindsightService import hindsight_service


async def get_memory_recent(user: dict):
    profile = get_user_profile(user['userId'])
    result = hindsight_service.recall_memory({
        'userId': user['userId'],
        'businessType': profile.get('businessType', 'distributor'),
        'query': 'recent verified operational experiences',
    })
    return result.get('memories', []) if result.get('status') not in {'fallback', 'error'} else []


async def recall_memory(query: str, user: dict):
    profile = get_user_profile(user['userId'])
    memory = hindsight_service.recall_memory({'userId': user['userId'], 'businessType': profile.get('businessType', 'distributor'), 'query': query})
    if memory.get('status') == 'fallback':
        return {'historical_memory': 'Historical memory currently unavailable.', 'source': 'fallback'}
    return memory


async def reflect_memory(context: dict, user: dict):
    profile = get_user_profile(user['userId'])
    memory = hindsight_service.reflect_memory({**context, 'userId': user['userId'], 'businessType': profile.get('businessType', 'distributor')})
    if memory.get('status') == 'fallback':
        return {'reflection': 'Historical memory currently unavailable.', 'source': 'fallback'}
    return memory


async def get_memory_stats(user: dict):
    memories = await get_memory_recent(user)
    return {
        'total_memories': len(memories),
        'recent_patterns': [item['pattern'] for item in memories],
        'successful_interventions': sum(1 for item in memories if item.get('outcome') == 'successful'),
        'unsuccessful_interventions': sum(1 for item in memories if item.get('outcome') in {'declined', 'unsuccessful'}),
    }
