from fastapi import APIRouter, Depends
from core.auth import get_current_user
from pydantic import BaseModel, Field

from controllers.recommendationController import apply_recommendation, record_recommendation_outcome

router = APIRouter(prefix='/recommendations', tags=['recommendations'])


class OutcomeRequest(BaseModel):
    before_minutes: float = Field(gt=0)
    after_minutes: float = Field(gt=0)


@router.post('/{recommendation_id}/apply')
async def apply(recommendation_id: str, current_user: dict = Depends(get_current_user)):
    return apply_recommendation(recommendation_id, current_user)


@router.post('/{recommendation_id}/outcome')
async def outcome(recommendation_id: str, payload: OutcomeRequest, current_user: dict = Depends(get_current_user)):
    return record_recommendation_outcome(recommendation_id, payload.before_minutes, payload.after_minutes, current_user)