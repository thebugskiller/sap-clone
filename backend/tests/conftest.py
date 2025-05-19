import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db.database import Base
from app.services.file_service import FileService
import os
import sys
import shutil

# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_session(test_db_engine):
    # Clear all tables before each test
    Base.metadata.drop_all(bind=test_db_engine)
    Base.metadata.create_all(bind=test_db_engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def test_client():
    return TestClient(app)

@pytest.fixture(scope="function")
def test_upload_dir():
    test_dir = "test_uploads"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.fixture(scope="function")
def file_service(test_upload_dir):
    return FileService(upload_dir=test_upload_dir) 