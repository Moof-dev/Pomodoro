from dataclasses import dataclass

import pytest


@dataclass
class FakeTaskRepository:
    task_models_factory: any
    faker: any

    async def get_tasks(self, user_id: int):
        return [self.task_models_factory.build(user_id=user_id) for _ in range(5)]

    async def get_task(self, task_id: int, user_id: int):
        return self.task_models_factory.build(id=task_id, user_id=user_id)

    async def get_user_task(self, user_id: int, task_id: int):
        return self.task_models_factory.build(id=task_id, user_id=user_id)

    async def create_task(self, task, user_id: int) -> int:
        return self.faker.random_int(min=1, max=1000)

    async def update_task_name(self, task_id: int, name: str, user_id: int):
        return self.task_models_factory.build(id=task_id, user_id=user_id, name=name)

    async def delete_task(self, task_id: int, user_id: int):
        pass

    async def get_tasks_by_category_name(self, category_name: str):
        pass

@pytest.fixture
def mock_task_repository(task_models_factory, faker):
    return FakeTaskRepository(task_models_factory=task_models_factory, faker=faker)