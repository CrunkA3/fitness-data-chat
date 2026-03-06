from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all database tables."""
    # Import models to register them with Base
    from app.models import activity, user  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
