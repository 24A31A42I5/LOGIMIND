from fastapi import APIRouter
from pydantic import BaseModel

from controllers.memoryController import get_memory_recent, get_memory_stats, recall_memory, reflect_memory

router = APIRouter(prefix='/memory', tags=['memory'])


class RecallRequest(BaseModel):
    query: str


class ReflectRequest(BaseModel):
    context: dict


@router.get('/recent')
async def recent_memory():
    return await get_memory_recent()


@router.post('/recall')
async def recall(payload: RecallRequest):
    return await recall_memory(payload.query)


@router.post('/reflect')
async def reflect(payload: ReflectRequest):
    return await reflect_memory(payload.context)


@router.get('/stats')
async def stats():
    return await get_memory_stats()
