from fastapi import APIRouter

from controllers.analyticsController import (
    get_analytics_areas,
    get_analytics_daily,
    get_analytics_hotspots,
    get_analytics_monthly,
    get_analytics_overall,
    get_analytics_trends,
)

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/overall')
async def overall():
    return await get_analytics_overall()


@router.get('/daily')
async def daily():
    return await get_analytics_daily()


@router.get('/monthly')
async def monthly():
    return await get_analytics_monthly()


@router.get('/areas')
async def areas():
    return await get_analytics_areas()


@router.get('/hotspots')
async def hotspots():
    return await get_analytics_hotspots()


@router.get('/trends')
async def trends():
    return await get_analytics_trends()
