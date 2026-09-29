from services.recommendationService import generate_investigation, get_today_insights


async def get_insight_summary():
    return get_today_insights()


async def investigate_area(area: str):
    return generate_investigation(area)
