from services.analyticsService import (
    get_area_analytics,
    get_daily_analytics,
    get_hotspots,
    get_monthly_analytics,
    get_overall_analytics,
    get_trends,
)


async def get_analytics_overall():
    return get_overall_analytics()


async def get_analytics_daily():
    return get_daily_analytics()


async def get_analytics_monthly():
    return get_monthly_analytics()


async def get_analytics_areas():
    return get_area_analytics()


async def get_analytics_hotspots():
    return get_hotspots()


async def get_analytics_trends():
    return get_trends()
