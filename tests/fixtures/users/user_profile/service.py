import pytest

from app.users.auth.client import MailClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService





@pytest.fixture
def mock_user_service(mock_auth_service,mock_user_repository):
    return UserService(
        user_repository=mock_user_repository,
        auth_service=mock_auth_service
    )

@pytest.fixture
def user_service(get_db_session, settings, google_client):
    return UserService(
        user_repository=UserRepository(db_session=get_db_session),
        auth_service=AuthService(
            user_repository=UserRepository(db_session=get_db_session),
            settings=settings,
            google_client=google_client,
            mail_client=MailClient()
        )
    )