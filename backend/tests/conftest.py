import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from database import Base
from app.models import GameCreate
from app.services import game_service

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest_asyncio.fixture
async def async_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
def test_client():
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient() as client:
        app_client = TestClient(app)
        client.base_url = "http://testserver"
        client.app = app_client.app
        yield client

@pytest_asyncio.fixture
async def populate_db(async_session):
    game_data = GameCreate(
        round="1",
        is_playoff=False,
        series_id=1,
        game_date="2024-01-01",
        team_1_id=1,
        team_2_id=2,
        score_1_1=10,
        score_1_2=5,
        score_2_1=15,
        score_2_2=10
    )
    await game_service.create_game(async_session, game_data)
    await async_session.commit()

