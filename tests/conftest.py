from src.main import app
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.app.api.deps import get_db
from src.app.models.user import User
from src.app.models.task import Task

@pytest.fixture(scope="function")
def override_get_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                           "check_same_thread": False})
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    User.metadata.create_all(bind=engine)
    Task.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        app.dependency_overrides[get_db] = lambda: session
        yield session
    finally:
        session.close()
        app.dependency_overrides.pop(get_db)