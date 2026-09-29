from fastapi import APIRouter
from pydantic import BaseModel, Field

from controllers.demoController import (
    close_demo_day,
    load_demo_day,
    reset_demo,
    trigger_area_c_delay,
    trigger_failed_delivery,
    trigger_successful_intervention,
)

router = APIRouter(prefix='/day', tags=['demo'])


class LoadDayRequest(BaseModel):
    day: int = Field(1, ge=1, le=30)


@router.post('/reset')
async def reset():
    return reset_demo()


@router.post('/load')
async def load(payload: LoadDayRequest):
    return load_demo_day(payload.day)


@router.post('/trigger-delay')
async def trigger_delay():
    return trigger_area_c_delay()


@router.post('/trigger-failure')
async def trigger_failure():
    return trigger_failed_delivery()


@router.post('/trigger-intervention')
async def trigger_intervention():
    return trigger_successful_intervention()


@router.post('/close')
async def close():
    return close_demo_day()