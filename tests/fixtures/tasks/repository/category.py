from dataclasses import dataclass

import pytest

from app.infrastructure.database.models import Categories


@dataclass
class FakeTaskCategoryRepository:
    categories_models: any

    async def get_category(self, category_id: int, user_id: int) -> Categories | None:
        return self.categories_models(id=category_id, user_id=user_id)


    async def get_categories(self, user_id: int) -> list[Categories] | None:
        return [self.categories_models(user_id=user_id) for _ in range(5)]

    async def create_category(self, name: str, user_id: int) -> int:
        return 1

    async def delete_category(self, category_id: int, user_id: int) -> None:
        pass

@pytest.fixture
def mock_category_repository(task_categories_models_factory):
    return FakeTaskCategoryRepository(categories_models=task_categories_models_factory)