from sqlalchemy.orm import Session

from app.config import settings
from app.models.activity import Activity


class StravaService:
    """Service for Strava API integration."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client_id = settings.strava_client_id
        self.client_secret = settings.strava_client_secret

    async def exchange_code(self, code: str, user_id: int) -> None:
        """Exchange OAuth code for access token."""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.strava.com/oauth/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            token_data = response.json()

        from app.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, email=f"user{user_id}@example.com")
            self.db.add(user)

        user.strava_token = token_data.get("access_token")
        user.strava_refresh_token = token_data.get("refresh_token")
        self.db.commit()

    async def get_activities(self, user_id: int, limit: int = 30) -> list[dict]:
        """Fetch activities from Strava API."""
        from app.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.strava_token:
            raise ValueError("User not connected to Strava")

        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers={"Authorization": f"Bearer {user.strava_token}"},
                params={"per_page": limit},
            )
            response.raise_for_status()
            return list(response.json())

    async def sync_activities(self, user_id: int) -> int:
        """Sync Strava activities to the database."""
        activities_data = await self.get_activities(user_id=user_id, limit=100)
        count = 0

        for data in activities_data:
            existing = (
                self.db.query(Activity)
                .filter(
                    Activity.user_id == user_id,
                    Activity.external_id == str(data["id"]),
                    Activity.source == "strava",
                )
                .first()
            )

            if not existing:
                from datetime import datetime

                activity = Activity(
                    user_id=user_id,
                    external_id=str(data["id"]),
                    source="strava",
                    name=data.get("name"),
                    activity_type=data.get("type"),
                    start_date=datetime.fromisoformat(
                        data["start_date"].replace("Z", "+00:00")
                    ) if data.get("start_date") else None,
                    distance_meters=data.get("distance"),
                    duration_seconds=data.get("moving_time"),
                    elevation_gain_meters=data.get("total_elevation_gain"),
                    avg_heart_rate=data.get("average_heartrate"),
                    max_heart_rate=data.get("max_heartrate"),
                    avg_speed_mps=data.get("average_speed"),
                    max_speed_mps=data.get("max_speed"),
                    calories=data.get("calories"),
                )
                self.db.add(activity)
                count += 1

        self.db.commit()
        return count
