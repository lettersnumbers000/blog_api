import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["CELERY_EAGER"] = "true"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.limiter import limiter
from app.main import app


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    limiter.reset()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
