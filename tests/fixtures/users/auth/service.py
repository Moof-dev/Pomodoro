import pytest

from app.settings import Setting
from app.users.auth.service import AuthService



@pytest.fixture
def auth_service(google_client,user_repository):
    return AuthService(
        user_repository=user_repository,
        settings=Setting(),
        google_client=google_client
    )