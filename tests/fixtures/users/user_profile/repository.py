from dataclasses import dataclass


import pytest

from app.users.user_profile.repository import UserRepository


@dataclass
class FakeUserRepository:
    user_profile_factory: any

    async def get_user_by_email(self, email: str):
        user = self.user_profile_factory.build()
        return user

    async def get_user_by_username(self, username: str):
        user = self.user_profile_factory.build()
        return user

    async def create_user(self, user):
        user = self.user_profile_factory.build()
        return user

    async def get_user(self, user_id: int):
        user = self.user_profile_factory.build()
        return user

@pytest.fixture
def mock_user_repository(user_profile_factory):
    return FakeUserRepository(user_profile_factory=user_profile_factory)

@pytest.fixture
def user_repository(get_db_session):
    return UserRepository(db_session=get_db_session)