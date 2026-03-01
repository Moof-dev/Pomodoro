from dataclasses import dataclass


import pytest


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
def user_repository(user_profile_factory):
    return FakeUserRepository(user_profile_factory=user_profile_factory)
