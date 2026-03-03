import asyncio

import pytest
from sqlalchemy import select, insert


from app.users.auth.schema import GoogleUserData
from app.infrastructure.database.models import UserProfile, Tasks, Categories

pytest_plugins = [
    "tests.fixtures.users.auth.service",
    "tests.fixtures.users.auth.clients",
    "tests.fixtures.users.user_profile.repository",
    "tests.fixtures.users.user_profile.service",
    "tests.fixtures.users.user_profile.models",
    "tests.fixtures.tasks.models",
    "tests.fixtures.tasks.schema",
    "tests.fixtures.tasks.service",
    "tests.fixtures.tasks.repository.cache_task",
    "tests.fixtures.tasks.repository.tasks",
    "tests.fixtures.tasks.repository.category",

    "tests.fixtures.infrastructure",
]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

EXIST_GOOGLE_USER_ID = 20
EXIST_GOOGLE_USER_EMAIL = "moof.error@gmail.com"

@pytest.fixture
def google_user_info_data(faker) -> GoogleUserData:
    return GoogleUserData(
        id=EXIST_GOOGLE_USER_ID,
        email=EXIST_GOOGLE_USER_EMAIL,
        verified_email=faker.boolean(),
        name=faker.name(),
        access_token=faker.sha256()
    )


async def create_test_user_in_db(user_model: UserProfile, db_session) -> int:
    session = db_session

    async with session as session:
        session.add(user_model)
        await session.commit()
        user_id = user_model.id

    return user_id


async def create_test_category_in_db(category_model: Categories, db_session) -> int:
    session = db_session

    async with session as session:
        session.add(category_model)
        await session.commit()
        category_id = category_model.id

    return category_id


async def create_test_task_in_db(task_model: Tasks, db_session) -> Tasks | None:
    session = db_session

    async with session as session:
        session.add(task_model)
        await session.commit()
    return task_model