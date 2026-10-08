from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from pydantic import BaseModel, Field

from controllers.recommendationController import apply_recommendation, record_recommendation_outcome

router = APIRouter(prefix='/recommendations', tags=['recommendations'])


class OutcomeRequest(BaseModel):
    metrics_before: dict[str, float] = Field(default_factory=dict)
    metrics_after: dict[str, float] = Field(default_factory=dict)
    notes: str = ''
    before_minutes: float | None = Field(default=None, gt=0)
    after_minutes: float | None = Field(default=None, gt=0)


@router.post('/{recommendation_id}/apply')
async def apply(recommendation_id: str, current_user: dict = Depends(get_current_user)):
    return apply_recommendation(recommendation_id, current_user)


@router.post('/{recommendation_id}/outcome')
async def outcome(recommendation_id: str, payload: OutcomeRequest, current_user: dict = Depends(get_current_user)):
    before = payload.metrics_before or ({'delivery_time': payload.before_minutes} if payload.before_minutes is not None else {})
    after = payload.metrics_after or ({'delivery_time': payload.after_minutes} if payload.after_minutes is not None else {})
    if not before or not after:
        raise HTTPException(status_code=400, detail='Provide metrics_before and metrics_after')
    return record_recommendation_outcome(recommendation_id, before, after, payload.notes, current_user)