from core.database import get_user_profile
from services.recommendationService import generate_investigation, get_today_insights


async def get_insight_summary(user: dict):
    profile = get_user_profile(user['userId'])
    return get_today_insights(profile.get('businessType', 'distributor'), user['userId'])


async def investigate_area(area: str, user: dict):
    profile = get_user_profile(user['userId'])
    return generate_investigation(area, profile.get('businessType', 'distributor'), user['userId'], profile.get('businessName', ''))
