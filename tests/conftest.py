
pytest_plugins = [
    "tests.fixtures.faker",
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

    "tests.fixtures.settings",
]