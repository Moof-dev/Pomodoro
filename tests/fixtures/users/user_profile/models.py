
import factory.fuzzy
from pytest_factoryboy import register

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


@register(_name="user_profile")
class UserProfileFactory(factory.Factory):

    class Meta:
        model = UserProfile

    id = factory.Faker("random_int")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    name = factory.Faker("name")
    password = factory.Faker("password")
    google_access_token = factory.Faker("sha256")


@register(_name="user_create")
class UserCreateFactory(factory.Factory):
    class Meta:
        model = UserCreateSchema

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    name = factory.Faker("name")
    google_access_token = factory.Faker("sha256")

