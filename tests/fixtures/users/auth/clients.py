from dataclasses import dataclass

import httpx
import pytest

from app.settings import Setting
from app.users.auth.schema import GoogleUserData



@dataclass
class FakeGoogleClient:
    settings: Setting
    async_client: httpx.AsyncClient
    google_user_info_data: GoogleUserData


    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return self.google_user_info_data


    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"



@pytest.fixture
def google_client(google_user_info_data):
    return FakeGoogleClient(settings=Setting(), async_client=httpx.AsyncClient(),
                            google_user_info_data=google_user_info_data)
