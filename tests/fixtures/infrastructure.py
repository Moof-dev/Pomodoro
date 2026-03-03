import pytest

from redis.asyncio import Redis
from faker import Factory as FakerFactory
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from app.settings import Setting
from app.infrastructure.database.database import Base





@pytest.fixture
def settings():
    return Setting()

@pytest.fixture
def faker():
    return FakerFactory.create()




engine = create_async_engine(url="postgresql+asyncpg://postgres-test:password@localhost:5442/pomodoro-test",
                             future=True, echo=False, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


@pytest.fixture(scope="function", autouse=True)
async def init_model(event_loop):
    async with engine.begin() as  conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    yield AsyncSessionFactory()


@pytest.fixture(scope="function")
async def get_redis():
    client = Redis(host="localhost", port=6389, db=0, decode_responses=True)
    await client.ping()
    yield client
    await client.flushdb()
    await client.aclose()






