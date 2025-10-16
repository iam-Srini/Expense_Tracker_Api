import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.db.models import Base
from app.db.session import get_db
from app.core.config import settings
from app.main import app
from fastapi.testclient import TestClient

# Create a new database session for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine) 

@pytest.fixture(autouse=True)
def clear_data():
    # Clear data before each test
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
