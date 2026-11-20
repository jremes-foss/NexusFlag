import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.db import get_db, Base
from app.core.limiter import limiter
from tests.factories import UserFactory, CategoryFactory, ChallengeFactory

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def db_engine():
    # StaticPool + check_same_thread=False keeps a single shared in-memory DB
    # alive across FastAPI TestClient threads and pytest fixtures
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    # Link factories to this specific test session
    UserFactory._meta.sqlalchemy_session = session
    CategoryFactory._meta.sqlalchemy_session = session
    ChallengeFactory._meta.sqlalchemy_session = session

    yield session
    session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def disable_rate_limit_by_default():
    limiter.enabled = False
    yield
    limiter.enabled = True
