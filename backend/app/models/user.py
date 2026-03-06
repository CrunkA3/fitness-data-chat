from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    strava_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    strava_refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    strava_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    garmin_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    garmin_password: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    activities: Mapped[list["Activity"]] = relationship(  # type: ignore[name-defined]
        "Activity", back_populates="user", cascade="all, delete-orphan"
    )
