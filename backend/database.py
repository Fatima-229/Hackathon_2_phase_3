from sqlmodel import create_engine, Session
from config import settings
from typing import Generator


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=True  # Set to True to see SQL queries in the logs
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.
    This function is meant to be used as a FastAPI dependency.
    """
    with Session(engine) as session:
        yield session


# Convenience function to create tables
def create_tables():
    """
    Create all tables defined in the models.
    This should typically be called once at application startup.
    """
    from sqlmodel import SQLModel
    from models.user import User
    from models.task import Task
    from models.conversation import Conversation
    from models.message import Message

    # Register all models
    SQLModel.metadata.create_all(engine)