from unittest.mock import AsyncMock
import pytest

from app.tasks.schema import TaskSchema, TaskCreateSchema


@pytest.mark.asyncio
async def test_get_tasks__success_from_cache(mock_task_service):
    tasks = await mock_task_service.get_tasks()

    assert isinstance(tasks[0], TaskSchema)

@pytest.mark.asyncio
async def test_get_tasks__success_from_db(mock_task_service):
    mock_task_service.task_cache.get_tasks = AsyncMock(return_value=None)
    mock_task_service.task_cache.set_tasks = AsyncMock(warps=mock_task_service.task_cache.set_tasks)

    tasks = await mock_task_service.get_tasks()

    assert isinstance(tasks[0], TaskSchema)
    assert len(tasks) > 0

    mock_task_service.task_cache.get_tasks.assert_called_once()
    mock_task_service.task_cache.set_tasks.assert_called_once()

@pytest.mark.asyncio
async def test_create_task__success(mock_task_service):
    task = await mock_task_service.create_task(body=TaskCreateSchema, user_id=1)

    assert isinstance(task, TaskSchema)

@pytest.mark.asyncio
async def test_update_task_name__success(mock_task_service):
    task = await mock_task_service.update_task_name(task_id=1, user_id=1, name="test_name")

    assert isinstance(task, TaskSchema)
    assert task.name == "test_name"
    assert task.id == 1
    assert task.user_id == 1

@pytest.mark.asyncio
async def test_delete_task__success(mock_task_service):
    mock_task_service.task_repository.delete_task = AsyncMock(warp=mock_task_service.task_repository.delete_task)

    await mock_task_service.delete_task(task_id=1, user_id=1)

    mock_task_service.task_repository.delete_task.assert_called_once()



