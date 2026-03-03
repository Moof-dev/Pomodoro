from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema




async def test_create_user__success(mock_user_service, faker):
    user_login = await mock_user_service.create_user(body=UserCreateSchema(
        username=faker.user_name(),
        password=faker.password()
    ))

    assert isinstance(user_login, UserLoginSchema)



