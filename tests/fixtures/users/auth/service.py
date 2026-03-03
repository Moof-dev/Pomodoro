import pytest

from app.settings import Setting
from app.users.auth.client import MailClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest.fixture
def mock_auth_service(google_client,mock_user_repository):
    return AuthService(
        user_repository=mock_user_repository,
        settings=Setting(),
        google_client=google_client,
        mail_client=MailClient()
    )

@pytest.fixture
def auth_service(google_client, get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings = Setting(),
        google_client = google_client,
        mail_client = MailClient()
    )