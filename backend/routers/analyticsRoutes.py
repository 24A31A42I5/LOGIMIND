from fastapi import APIRouter, Depends
from core.auth import get_current_user
from core.database import get_user_profile

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
async def overall(current_user: dict = Depends(get_current_user)):
    return await get_analytics_overall(current_user)


@router.get('/daily')
async def daily(current_user: dict = Depends(get_current_user)):
    return await get_analytics_daily(current_user)


@router.get('/monthly')
async def monthly(current_user: dict = Depends(get_current_user)):
    return await get_analytics_monthly(current_user)


@router.get('/areas')
async def areas(current_user: dict = Depends(get_current_user)):
    return await get_analytics_areas(current_user)


@router.get('/hotspots')
async def hotspots(current_user: dict = Depends(get_current_user)):
    return await get_analytics_hotspots(current_user)


@router.get('/trends')
async def trends(current_user: dict = Depends(get_current_user)):
    return await get_analytics_trends(current_user)
