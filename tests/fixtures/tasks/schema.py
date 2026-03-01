import factory.fuzzy
from pytest_factoryboy import register

from app.tasks.schema import TaskSchema, TaskCategorySchema


@register(_name="task_schema")
class TaskSchemaFactory(factory.Factory):
    class Meta:
        model = TaskSchema

    id = factory.Faker("random_int")
    name = factory.Faker("word")
    pomodoro_count = factory.Faker("random_int", min=1, max=20)
    category_id = factory.Faker("random_int", min=1, max=1000 )
    user_id = factory.Faker("random_int")


@register(_name= "categories_schema")
class TaskCategoriesSchemaFactory(factory.Factory):
    class Meta:
        model = TaskCategorySchema

    id = factory.Faker("random_int", min=1, max=1000 )
    type = factory.Faker("word")
    name = factory.Faker("word")

