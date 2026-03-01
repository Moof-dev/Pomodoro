import factory.fuzzy
from pytest_factoryboy import register

from app.tasks.models import Tasks, Categories


@register(_name="task_model")
class TaskModelsFactory(factory.Factory):

    class Meta:
        model = Tasks

    id = factory.Faker("random_int")
    name = factory.Faker("word")
    pomodoro_count = factory.Faker("random_int", min=1, max=20)
    category_id = factory.Faker("random_int", min=1, max=1000 )
    user_id = factory.Faker("random_int")


@register(_name= "categories_models")
class TaskCategoriesModelsFactory(factory.Factory):

    class Meta:
        model = Categories

    id = factory.Faker("random_int", min=1, max=1000 )
    type = factory.Faker("word")
    name = factory.Faker("word")

