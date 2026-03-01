import datetime as dt

import pytest
from jose import jwt


pytest.mark = pytest.mark.asyncio

async def test_login__success(auth_service, user_repository):
    username = "true_username"
    password = "true_password"
    user = await user_repository.get_user_by_username(username)
    user.password = password
    auth_service._validate_auth_user(user=user, password=password)
    access_token = auth_service.generate_access_token(user_id=user.id)

    assert auth_service.get_user_id_from_access_token(access_token) == user.id

async def test_get_google_redirect_url__success(auth_service, settings):
    settings_google_redirect_url = settings.google_redirect_url

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert auth_service_google_redirect_url == settings_google_redirect_url

async def test_get_google_redirect_url__fail(auth_service, settings):
    settings_google_redirect_url = "https://fake_google_redirect_url.com"

    auth_service_google_redirect_url = auth_service.get_google_redirect_url()

    assert auth_service_google_redirect_url != settings_google_redirect_url

async def test_google_auth__success(auth_service):
    code="fake_code"

    user = await auth_service.google_auth(code=code)
    decoded_user_id = auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id


async def test_generate_access_token__success(auth_service, settings):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(access_token,settings.JWT_SECRET_KEY,algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get("expire"), tz=dt.UTC)

    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC) > dt.timedelta(days=6))
    assert decoded_user_id == user_id

async def test_get_user_id_from_access_token__success(auth_service):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)

    assert auth_service.get_user_id_from_access_token(access_token) == user_id

