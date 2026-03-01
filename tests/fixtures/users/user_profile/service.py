import pytest

from app.users.user_profile.service import UserService





@pytest.fixture
def mock_user_service(mock_auth_service,mock_user_repository):
    return UserService(
        user_repository=mock_user_repository,
        auth_service=mock_auth_service
    )