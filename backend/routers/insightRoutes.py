from fastapi import APIRouter, Depends
from core.auth import get_current_user
from pydantic import BaseModel

from controllers.insightController import get_insight_summary, investigate_area

router = APIRouter(prefix='/insights', tags=['insights'])


class InvestigationRequest(BaseModel):
    area: str = 'Area C'


@router.get('/today')
async def today_insights(current_user: dict = Depends(get_current_user)):
    return await get_insight_summary(current_user)


@router.post('/investigate')
async def investigate(payload: InvestigationRequest, current_user: dict = Depends(get_current_user)):
    return await investigate_area(payload.area, current_user)
