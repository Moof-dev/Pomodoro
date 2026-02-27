
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.settings import Setting

engine = create_async_engine(url=Setting().db_url, future=True, echo=False, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session