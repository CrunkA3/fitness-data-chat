from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.garmin_service import GarminService

router = APIRouter()


class GarminAuthRequest(BaseModel):
    email: str
    password: str
    user_id: int = 1


class SyncRequest(BaseModel):
    user_id: int = 1


@router.post("/auth")
async def garmin_auth(
    auth_request: GarminAuthRequest,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Authenticate with Garmin Connect."""
    garmin_service = GarminService(db=db)
    try:
        await garmin_service.authenticate(
            email=auth_request.email,
            password=auth_request.password,
            user_id=auth_request.user_id,
        )
        return {"status": "success", "message": "Garmin connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/activities")
async def get_garmin_activities(
    user_id: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Fetch Garmin activities for a user."""
    garmin_service = GarminService(db=db)
    try:
        activities = await garmin_service.get_activities(user_id=user_id, limit=limit)
        return activities
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/sync")
async def sync_garmin_activities(
    sync_request: SyncRequest,
    db: Session = Depends(get_db),
) -> dict[str, str | int]:
    """Sync Garmin activities to the database."""
    garmin_service = GarminService(db=db)
    try:
        count = await garmin_service.sync_activities(user_id=sync_request.user_id)
        return {"status": "success", "synced_count": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
