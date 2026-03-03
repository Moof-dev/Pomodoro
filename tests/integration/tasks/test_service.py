from winreg import error

import pytest
from sqlalchemy import select, insert, delete

from app.exception import BaseAppException
from app.tasks.schema import TaskSchema, TaskCategorySchema
from app.infrastructure.database.models import UserProfile, Tasks, Categories
from tests.conftest import create_test_user_in_db, create_test_category_in_db, create_test_task_in_db


async def test_get_tasks__success_in_db_and_in_cache(task_service, get_db_session, task_create_schema_factory):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    with pytest.raises(BaseAppException) as e:
        await task_service.get_tasks(user_id=user_id)
    for _ in range(5):
        task = task_create_schema_factory()
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=category_id,
            user_id=user_id
        )
        await create_test_task_in_db(task_model, db_session=get_db_session)

    tasks_in_db = await task_service.get_tasks(user_id=user_id)
    async with get_db_session as session:
        await session.execute(delete(Tasks))
        await session.commit()
    tasks_in_cache = await task_service.get_tasks(user_id=user_id)

    assert "not found" in str(e.value.detail)
    assert len(tasks_in_db) == 5 and len(tasks_in_cache) == 5
    assert isinstance(tasks_in_db[0], TaskSchema) and isinstance(tasks_in_cache[0], TaskSchema)
    assert (tasks_in_db[0].category_id == category_id and tasks_in_db[0].user_id == user_id) or (
            tasks_in_cache[0].category_id == category_id and tasks_in_cache[0].user_id == user_id)


async def test_get_task__success(task_service, get_db_session, task_create_schema_factory):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    with pytest.raises(BaseAppException) as e:
        await task_service.get_task(user_id=user_id, task_id=1000)
    task_schema = task_create_schema_factory()
    task_model = Tasks(
        name=task_schema.name,
        pomodoro_count=task_schema.pomodoro_count,
        category_id=category_id,
        user_id=user_id
    )
    fake_task = TaskSchema.model_validate(await create_test_task_in_db(task_model, db_session=get_db_session))
    task = await task_service.get_task(task_id=fake_task.id, user_id=user_id)

    assert "not found" in str(e.value.detail)
    assert isinstance(task, TaskSchema)
    assert fake_task == task

async def test_create_task__success(task_service, get_db_session, task_create_schema_factory):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    task_schema = task_create_schema_factory(category_id=category_id, user_id=user_id)
    task = await task_service.create_task(body=task_schema, user_id=user_id)

    assert isinstance(task, TaskSchema)
    assert task.user_id == user_id and task.category_id == category_id

async def test_update_task_name__success(task_service, get_db_session, task_create_schema_factory):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    task_schema = task_create_schema_factory()
    task_model = Tasks(
        name="fake name",
        pomodoro_count=task_schema.pomodoro_count,
        category_id=category_id,
        user_id=user_id
    )
    fake_task = await create_test_task_in_db(task_model, db_session=get_db_session)
    task = await task_service.update_task_name(task_id=fake_task.id, name="success name", user_id=user_id)

    assert isinstance(task, TaskSchema)
    assert task.user_id == user_id and task.category_id == category_id and task.name == "success name"

async def test_delete_task__success(task_service, get_db_session, task_create_schema_factory):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    task_schema = task_create_schema_factory()
    task_model = Tasks(
        name="fake name",
        pomodoro_count=task_schema.pomodoro_count,
        category_id=category_id,
        user_id=user_id
    )
    fake_task = await create_test_task_in_db(task_model, db_session=get_db_session)
    await task_service.delete_task(task_id=fake_task.id, user_id=user_id)
    async with get_db_session as session:
        task = (await session.execute(select(Tasks).where(Tasks.id == fake_task.id))).scalar_one_or_none()
        await session.commit()

    assert task == None


async def test_create_category__success(task_service, get_db_session):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category = await task_service.create_category(user_id=user_id, name="test_category")

    assert isinstance(category, TaskCategorySchema)
    assert category.user_id == user_id and category.name == "test_category"

async def test_get_category__success(task_service, get_db_session):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test_category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    category = await task_service.get_category(category_id=category_id, user_id=user_id)
    with pytest.raises(BaseAppException) as e:
        error_categories = await task_service.get_category(category_id=10000, user_id=user_id)

    assert "not found" in str(e.value.detail)
    assert isinstance(category, TaskCategorySchema)
    assert category.user_id == user_id and category.name == "test_category"

async def test_get_categories__success(task_service, get_db_session, faker):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    with pytest.raises(BaseAppException) as e:
        error_categories = await task_service.get_categories(user_id=user_id)
    for _ in range(5):
        category_model = Categories(name=faker.word(), user_id=user_id)
        await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    categories = await task_service.get_categories(user_id=user_id)

    assert "not found" in str(e.value.detail)
    assert isinstance(categories[0], TaskCategorySchema)
    assert categories[0].user_id == user_id
    assert len(categories) == 5

async def test_delete_category__success(task_service, get_db_session, faker):
    user_model = UserProfile(username="test_user", password="password")
    user_id = await create_test_user_in_db(user_model=user_model, db_session=get_db_session)
    category_model = Categories(name="test_category", user_id=user_id)
    category_id = await create_test_category_in_db(category_model=category_model, db_session=get_db_session)
    await task_service.delete_category(category_id=category_id, user_id=user_id)
    async with get_db_session as session:
        category = (await session.execute(select(Categories).where(Categories.id == category_id))).scalar_one_or_none()
        await session.commit()

    with pytest.raises(BaseAppException) as e:
        await task_service.delete_category(category_id=category_id, user_id=user_id)
    assert "not found" in str(e.value.detail)
    assert category == None

