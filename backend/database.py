"""
QR Inventory MVP - Database Configuration
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./dev.db"

# Create engine
# For SQLite: check_same_thread=False allows multiple threads
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {},
    echo=True if os.getenv('FLASK_DEBUG', 'True').lower() == 'true' else False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Usage: db = get_db()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database (create tables).
    Called when app starts or in migrations.
    """
    Base.metadata.create_all(bind=engine)


def test_connection():
    """
    Test database connection.
    Returns True if successful, False otherwise.
    """
    try:
        connection = engine.connect()
        connection.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
