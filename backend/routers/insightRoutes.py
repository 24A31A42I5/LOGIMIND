from fastapi import APIRouter
from pydantic import BaseModel

from controllers.insightController import get_insight_summary, investigate_area

router = APIRouter(prefix='/insights', tags=['insights'])


class InvestigationRequest(BaseModel):
    area: str = 'Area C'


@router.get('/today')
async def today_insights():
    return await get_insight_summary()


@router.post('/investigate')
async def investigate(payload: InvestigationRequest):
    return await investigate_area(payload.area)
