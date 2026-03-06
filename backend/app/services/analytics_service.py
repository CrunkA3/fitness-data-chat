from datetime import datetime

from sqlalchemy.orm import Session

from app.models.activity import Activity


class AnalyticsService:
    """Service for analytics and data analysis."""

    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_summary(self, user_id: int) -> dict:
        """Get summary statistics for a user's activities."""
        activities = (
            self.db.query(Activity)
            .filter(Activity.user_id == user_id)
            .all()
        )

        if not activities:
            return {
                "total_activities": 0,
                "total_distance_km": 0.0,
                "total_duration_hours": 0.0,
                "avg_heart_rate": None,
                "activity_types": {},
                "recent_activities": [],
            }

        total_distance = sum(
            (a.distance_meters or 0) for a in activities
        ) / 1000.0
        total_duration = sum(
            (a.duration_seconds or 0) for a in activities
        ) / 3600.0

        heart_rates = [a.avg_heart_rate for a in activities if a.avg_heart_rate]
        avg_hr = sum(heart_rates) / len(heart_rates) if heart_rates else None

        activity_types: dict[str, int] = {}
        for activity in activities:
            activity_type = activity.activity_type or "Unknown"
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1

        recent = sorted(
            activities,
            key=lambda a: a.start_date or datetime.min,
            reverse=True,
        )[:5]

        recent_activities = [
            {
                "id": a.id,
                "name": a.name,
                "type": a.activity_type,
                "date": a.start_date.isoformat() if a.start_date else None,
                "distance_km": (a.distance_meters or 0) / 1000.0,
                "duration_minutes": (a.duration_seconds or 0) / 60.0,
            }
            for a in recent
        ]

        return {
            "total_activities": len(activities),
            "total_distance_km": round(total_distance, 2),
            "total_duration_hours": round(total_duration, 2),
            "avg_heart_rate": round(avg_hr, 1) if avg_hr else None,
            "activity_types": activity_types,
            "recent_activities": recent_activities,
        }

    async def execute_query(self, query: str, user_id: int) -> dict:
        """Execute a custom analytics query."""
        # For safety, we use SQLAlchemy ORM rather than raw SQL from user input
        # This is a simplified implementation
        activities = (
            self.db.query(Activity)
            .filter(Activity.user_id == user_id)
            .all()
        )

        if not activities:
            return {"results": [], "message": "No activities found"}

        # Convert to pandas for complex analysis
        try:
            import pandas as pd

            data = [
                {
                    "id": a.id,
                    "name": a.name,
                    "type": a.activity_type,
                    "date": a.start_date,
                    "distance_km": (a.distance_meters or 0) / 1000.0,
                    "duration_min": (a.duration_seconds or 0) / 60.0,
                    "avg_hr": a.avg_heart_rate,
                    "max_hr": a.max_heart_rate,
                    "calories": a.calories,
                }
                for a in activities
            ]

            df = pd.DataFrame(data)
            query_lower = query.lower()

            if "heart rate" in query_lower or "hr" in query_lower:
                hr_stats = df["avg_hr"].describe().to_dict()
                return {"results": hr_stats, "message": "Heart rate statistics"}
            elif "distance" in query_lower:
                dist_stats = df["distance_km"].describe().to_dict()
                return {"results": dist_stats, "message": "Distance statistics"}
            elif "type" in query_lower or "activity" in query_lower:
                type_counts = df["type"].value_counts().to_dict()
                return {"results": type_counts, "message": "Activity type breakdown"}
            else:
                # Default: return general stats
                summary = {
                    "count": len(df),
                    "total_distance_km": df["distance_km"].sum(),
                    "avg_duration_min": df["duration_min"].mean(),
                }
                return {"results": summary, "message": "General statistics"}

        except ImportError:
            # Fallback without pandas
            return {
                "results": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.activity_type,
                    }
                    for a in activities[:10]
                ],
                "message": "Basic activity list",
            }
