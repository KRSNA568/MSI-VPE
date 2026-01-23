from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create SQLAlchemy Engine
# connect_args={"check_same_thread": False} is needed only for SQLite.
# It allows more than one thread to communicate with the database.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args,
    echo=settings.DATABASE_ECHO
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """Dependency for FastAPI Endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
