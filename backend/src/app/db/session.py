# AI Optimized by Skills Agent: SQLAlchemy engine/session skeleton for future PostgreSQL persistence.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# AI Optimized by Skills Agent: Engine is centralized so migrations and services share one contract.
engine = create_engine(settings.database_url, pool_pre_ping=True)


# AI Optimized by Skills Agent: Session factory will be injected into services and routes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
