from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database.db import get_db
from app.services.strava_service import StravaService

router = APIRouter()


class SyncRequest(BaseModel):
    user_id: int = 1


@router.get("/auth")
async def strava_auth() -> dict[str, str]:
    """Initiate Strava OAuth flow."""
    auth_url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={settings.strava_client_id}"
        "&response_type=code"
        f"&redirect_uri={settings.strava_redirect_uri}"
        "&approval_prompt=force"
        "&scope=read,activity:read_all"
    )
    return {"auth_url": auth_url}


@router.get("/callback")
async def strava_callback(code: str, db: Session = Depends(get_db)) -> dict[str, str]:
    """Handle Strava OAuth callback."""
    strava_service = StravaService(db=db)
    try:
        await strava_service.exchange_code(code=code, user_id=1)
        return {"status": "success", "message": "Strava connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/activities")
async def get_strava_activities(
    user_id: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Fetch Strava activities for a user."""
    strava_service = StravaService(db=db)
    try:
        activities = await strava_service.get_activities(user_id=user_id, limit=limit)
        return activities
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/sync")
async def sync_strava_activities(
    sync_request: SyncRequest,
    db: Session = Depends(get_db),
) -> dict[str, str | int]:
    """Sync Strava activities to the database."""
    strava_service = StravaService(db=db)
    try:
        count = await strava_service.sync_activities(user_id=sync_request.user_id)
        return {"status": "success", "synced_count": count}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
