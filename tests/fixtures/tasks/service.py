import pytest

from app.tasks.repository import TaskCategoryRepository, TaskRepository, TaskCache
from app.tasks.service import TaskService


@pytest.fixture
def mock_task_service(mock_task_repository,mock_task_cache, mock_category_repository):
    return TaskService(
        task_repository=mock_task_repository,
        task_cache=mock_task_cache,
        category_repository=mock_category_repository
    )

@pytest.fixture
def task_service(mock_task_cache, get_db_session, get_redis):
    return TaskService(
        task_repository=TaskRepository(
            db_session=get_db_session
        ),
        task_cache=TaskCache(redis=get_redis),
        category_repository=TaskCategoryRepository(
            db_session=get_db_session
        )
    )