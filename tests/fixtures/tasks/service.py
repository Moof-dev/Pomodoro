import pytest

from app.tasks.service import TaskService


@pytest.fixture
def mock_task_service(mock_task_repository,mock_task_cache):
    return TaskService(
        task_repository=mock_task_repository,
        task_cache=mock_task_cache
    )