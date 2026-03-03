import pytest

from sqlalchemy import insert, select

from app.exception import BaseAppException
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


async def test_base_create_user__success_not_exist_user(user_service):
    user = await user_service.create_user(UserCreateSchema(username="test_user", password="password"))

    assert isinstance(user, UserLoginSchema)

async def test_base_create_user__fail_exist_user(user_service, get_db_session):
    session = get_db_session
    username = "test_user"
    password = "password"
    query = insert(UserProfile).values(
        username=username,
        password=password
    )

    async with session as session:
        await session.execute(query)
        await session.commit()

    with pytest.raises(BaseAppException) as e:
        await user_service.create_user(UserCreateSchema(username="test_user", password="password"))
    assert "already exists" in str(e.value.detail)

