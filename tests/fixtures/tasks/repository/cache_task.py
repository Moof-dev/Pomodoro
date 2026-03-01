from dataclasses import dataclass

import pytest

from app.tasks.schema import TaskSchema


@dataclass
class FakeTaskCache:
    task_schema_factory: any


    async def get_tasks(self):
        return [self.task_schema_factory.build() for _ in range(5)]

    async def get_task(self, task_id: int):
        pass

    async def set_tasks(self, tasks: list[TaskSchema]):
        pass

@pytest.fixture
def task_cache(task_schema_factory):
    return FakeTaskCache(task_schema_factory=task_schema_factory)