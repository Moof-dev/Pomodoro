import asyncio

import pytest

from app.users.auth.schema import GoogleUserData

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