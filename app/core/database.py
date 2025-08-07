from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create engine with pooling and auto-reconnect
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,           # Number of connections to keep in the pool
    max_overflow=10,       # Extra connections beyond pool_size
    pool_timeout=30,       # Seconds to wait before giving up on a connection
    pool_recycle=1800,     # Reconnect every 30 min to avoid stale connections
    pool_pre_ping=True     # Test connection before using it
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
