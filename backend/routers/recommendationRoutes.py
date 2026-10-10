from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from pydantic import BaseModel, Field

from controllers.recommendationController import (
    apply_recommendation,
    execute_recommendation,
    record_recommendation_outcome,
)

router = APIRouter(prefix='/recommendations', tags=['recommendations'])


class OutcomeRequest(BaseModel):
    metrics_before: dict[str, float] = Field(default_factory=dict)
    metrics_after: dict[str, float] = Field(default_factory=dict)
    observation_ids: list[str] = Field(default_factory=list, min_length=1)
    notes: str = ''
    before_minutes: float | None = Field(default=None, gt=0)
    after_minutes: float | None = Field(default=None, gt=0)


class ExecutionRequest(BaseModel):
    shipment_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)


@router.post('/{recommendation_id}/apply')
async def apply(recommendation_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return apply_recommendation(recommendation_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post('/{recommendation_id}/execute')
async def execute(
    recommendation_id: str,
    payload: ExecutionRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        return execute_recommendation(
            recommendation_id,
            payload.shipment_id,
            payload.agent_id,
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post('/{recommendation_id}/outcome')
async def outcome(recommendation_id: str, payload: OutcomeRequest, current_user: dict = Depends(get_current_user)):
    before = payload.metrics_before or ({'delivery_time': payload.before_minutes} if payload.before_minutes is not None else {})
    after = payload.metrics_after or ({'delivery_time': payload.after_minutes} if payload.after_minutes is not None else {})
    if not before or not after:
        raise HTTPException(status_code=400, detail='Provide metrics_before and metrics_after')
    try:
        return record_recommendation_outcome(
            recommendation_id,
            before,
            after,
            payload.notes,
            current_user,
            payload.observation_ids,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc