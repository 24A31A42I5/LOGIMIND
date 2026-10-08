from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.auth import get_current_user
from services.analysisService import apply_analysis, generate_analysis


router = APIRouter(prefix='/analysis', tags=['analysis'])


class AnalysisRequest(BaseModel):
    period: str = Field(default='overall', pattern='^(today|week|month|overall)$')


@router.post('')
async def run_analysis(payload: AnalysisRequest, current_user: dict = Depends(get_current_user)):
    return generate_analysis(current_user, payload.period)


@router.post('/{analysis_id}/apply')
async def apply(analysis_id: str, current_user: dict = Depends(get_current_user)):
    result = apply_analysis(analysis_id, current_user)
    if result is None:
        raise HTTPException(status_code=404, detail='Analysis not found')
    return result