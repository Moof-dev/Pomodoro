import factory.fuzzy
from pytest_factoryboy import register

from app.tasks.schema import TaskSchema, TaskCategorySchema, TaskCreateSchema


@register(_name="task_schema")
class TaskSchemaFactory(factory.Factory):
    class Meta:
        model = TaskSchema

    id = factory.Faker("random_int")
    name = factory.Faker("word")
    pomodoro_count = factory.Faker("random_int", min=1, max=20)
    category_id = factory.Faker("random_int", min=1, max=1000 )
    user_id = factory.Faker("random_int")

@register(_name="task_create_schema")
class TaskCreateSchemaFactory(factory.Factory):
    class Meta:
        model =TaskCreateSchema

    name = factory.Faker("word")
    pomodoro_count = factory.Faker("random_int", min=1, max=1000)
    category_id = factory.Faker("random_int", min=1, max=1000)
    user_id = factory.Faker("random_int", min=1, max=1000)


@register(_name= "categories_schema")
class TaskCategoriesSchemaFactory(factory.Factory):
    class Meta:
        model = TaskCategorySchema

    id = factory.Faker("random_int", min=1, max=1000 )
    name = factory.Faker("word")
    user_id = factory.Faker("random_int", min=1, max=1000 )

