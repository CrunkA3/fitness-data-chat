from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    user_id: int = 1


@router.get("/summary")
async def get_summary(
    user_id: int = 1,
    db: Session = Depends(get_db),
) -> dict:
    """Get summary statistics for a user's activities."""
    analytics_service = AnalyticsService(db=db)
    try:
        return await analytics_service.get_summary(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/query")
async def custom_query(
    query_request: QueryRequest,
    db: Session = Depends(get_db),
) -> dict:
    """Execute a custom analytics query."""
    analytics_service = AnalyticsService(db=db)
    try:
        return await analytics_service.execute_query(
            query=query_request.query,
            user_id=query_request.user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
