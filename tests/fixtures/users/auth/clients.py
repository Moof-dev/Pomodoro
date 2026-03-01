from dataclasses import dataclass

import httpx
import pytest

from app.settings import Setting
from app.users.auth.schema import GoogleUserData

from faker import Factory as FakerFactory


faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Setting
    async_client: httpx.AsyncClient


    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()


    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"



@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Setting(), async_client=httpx.AsyncClient())


def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=faker.email(),
        verified_email=faker.boolean(),
        name=faker.name(),
        access_token=faker.sha256()
    )