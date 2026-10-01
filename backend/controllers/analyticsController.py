from core.database import get_user_profile
from services.analyticsService import (
    get_area_analytics,
    get_daily_analytics,
    get_hotspots,
    get_monthly_analytics,
    get_overall_analytics,
    get_trends,
)


def _context(user: dict) -> tuple[str, str]:
    profile = get_user_profile(user['userId'])
    return profile.get('businessType', 'distributor'), user['userId']


async def get_analytics_overall(user: dict):
    return get_overall_analytics(*_context(user))


async def get_analytics_daily(user: dict):
    return get_daily_analytics(*_context(user))


async def get_analytics_monthly(user: dict):
    return get_monthly_analytics(*_context(user))


async def get_analytics_areas(user: dict):
    return get_area_analytics(*_context(user))


async def get_analytics_hotspots(user: dict):
    return get_hotspots(*_context(user))


async def get_analytics_trends(user: dict):
    return get_trends(*_context(user))
