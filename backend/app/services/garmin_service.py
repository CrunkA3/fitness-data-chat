from sqlalchemy.orm import Session

from app.models.activity import Activity


class GarminService:
    """Service for Garmin Connect integration."""

    def __init__(self, db: Session) -> None:
        self.db = db

    async def authenticate(self, email: str, password: str, user_id: int) -> None:
        """Authenticate with Garmin Connect."""
        from garminconnect import Garmin

        client = Garmin(email, password)
        client.login()

        from app.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, email=email)
            self.db.add(user)

        user.garmin_email = email
        # NOTE: In production, encrypt the password before storing it.
        user.garmin_password = password
        self.db.commit()

    async def get_activities(self, user_id: int, limit: int = 30) -> list[dict]:
        """Fetch activities from Garmin Connect."""
        from app.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.garmin_email:
            raise ValueError("User not connected to Garmin")

        from garminconnect import Garmin

        # NOTE: In production, use a secrets manager or proper encryption instead of
        # storing plaintext passwords. This is a simplified implementation.
        if not user.garmin_password:
            raise ValueError("Garmin password not stored for this user")

        client = Garmin(user.garmin_email, user.garmin_password)

        activities = client.get_activities(0, limit)
        return list(activities)

    async def sync_activities(self, user_id: int) -> int:
        """Sync Garmin activities to the database."""
        activities_data = await self.get_activities(user_id=user_id, limit=100)
        count = 0

        for data in activities_data:
            activity_id = str(data.get("activityId", ""))
            existing = (
                self.db.query(Activity)
                .filter(
                    Activity.user_id == user_id,
                    Activity.external_id == activity_id,
                    Activity.source == "garmin",
                )
                .first()
            )

            if not existing:
                from datetime import datetime

                start_time_str = data.get("startTimeLocal", "")
                start_date = None
                if start_time_str:
                    try:
                        start_date = datetime.fromisoformat(start_time_str)
                    except ValueError:
                        pass

                activity = Activity(
                    user_id=user_id,
                    external_id=activity_id,
                    source="garmin",
                    name=data.get("activityName"),
                    activity_type=data.get("activityType", {}).get("typeKey"),
                    start_date=start_date,
                    distance_meters=data.get("distance"),
                    duration_seconds=int(data.get("duration", 0)),
                    elevation_gain_meters=data.get("elevationGain"),
                    avg_heart_rate=data.get("averageHR"),
                    max_heart_rate=data.get("maxHR"),
                    avg_speed_mps=data.get("averageSpeed"),
                    max_speed_mps=data.get("maxSpeed"),
                    calories=data.get("calories"),
                )
                self.db.add(activity)
                count += 1

        self.db.commit()
        return count
