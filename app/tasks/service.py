from dataclasses import dataclass


from app.exception import TaskNotFound, CategoryNotFound
from app.tasks.repository import TaskRepository, TaskCache, TaskCategoryRepository
from app.tasks.schema import TaskCreateSchema, TaskSchema, TaskCategorySchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    category_repository: TaskCategoryRepository
    task_cache: TaskCache

    async def get_tasks(self, user_id: int) -> list[TaskSchema]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = await self.task_repository.get_tasks(user_id=user_id)
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def get_task(self, task_id: int, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_task(task_id=task_id, user_id=user_id)
        task_schema = TaskSchema.model_validate(task)
        return task_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id=task_id, user_id=user_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id=task_id, name=name, user_id=user_id)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)


    async def create_category(self, name: str, user_id: int) -> TaskCategorySchema:
        category_id = await self.category_repository.create_category(name=name, user_id=user_id)
        category = await self.category_repository.get_category(user_id=user_id, category_id=category_id)
        return TaskCategorySchema.model_validate(category)

    async def get_category(self, category_id: int, user_id: int) -> TaskCategorySchema | None:
        category = await self.category_repository.get_category(user_id=user_id, category_id=category_id)
        category_schema= TaskCategorySchema.model_validate(category)
        return category_schema

    async def get_categories(self, user_id: int) -> list[TaskCategorySchema] | None:
        categories = await self.category_repository.get_categories(user_id=user_id)
        categories_schema = [TaskCategorySchema.model_validate(category) for category in categories]
        return categories_schema

    async def delete_category(self, category_id: int, user_id: int) -> None:
        category = await self.category_repository.get_category(user_id=user_id, category_id=category_id)
        if not category:
            raise CategoryNotFound
        await self.category_repository.delete_category(category_id=category_id, user_id=user_id)
