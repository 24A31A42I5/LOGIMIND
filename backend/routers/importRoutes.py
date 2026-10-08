from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from core.auth import get_current_user
from core.database import get_user_profile
from services.importService import import_csv


router = APIRouter(prefix='/imports', tags=['imports'])


@router.post('/{dataset}')
async def upload_csv(dataset: str, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    profile = get_user_profile(current_user['userId'])
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Upload a CSV file')
    try:
        return import_csv(await file.read(), profile.get('businessType', 'distributor'), dataset, current_user['userId'])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc