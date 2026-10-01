from fastapi import APIRouter, Depends
from core.auth import get_current_user
from pydantic import BaseModel

from controllers.memoryController import get_memory_recent, get_memory_stats, recall_memory, reflect_memory

router = APIRouter(prefix='/memory', tags=['memory'])


class RecallRequest(BaseModel):
    query: str


class ReflectRequest(BaseModel):
    context: dict


@router.get('/recent')
async def recent_memory(current_user: dict = Depends(get_current_user)):
    return await get_memory_recent(current_user)


@router.post('/recall')
async def recall(payload: RecallRequest, current_user: dict = Depends(get_current_user)):
    return await recall_memory(payload.query, current_user)


@router.post('/reflect')
async def reflect(payload: ReflectRequest, current_user: dict = Depends(get_current_user)):
    return await reflect_memory(payload.context, current_user)


@router.get('/stats')
async def stats(current_user: dict = Depends(get_current_user)):
    return await get_memory_stats(current_user)
