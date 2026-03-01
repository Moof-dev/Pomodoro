from sqlalchemy import select, insert

from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile
from tests.conftest import EXIST_GOOGLE_USER_ID, EXIST_GOOGLE_USER_EMAIL


async def test_base_login__success(auth_service, get_db_session):
    session = get_db_session
    username = "test_user"
    password = "test_password"
    user_id = 100
    query = insert(UserProfile).values(
        id=user_id,
        username=username,
        password=password
    )


    async with session as session:
        await session.execute(query)
        await session.commit()

    login_user = await auth_service.login(username=username, password=password)


    assert isinstance(login_user, UserLoginSchema)
    assert login_user.user_id == user_id


async def test_google_auth__login_not_exist_user(auth_service, get_db_session):
    code = "fake_code"
    query = select(UserProfile)

    async with get_db_session as session:
        users = (await session.execute(query)).scalars().all()
    user = await auth_service.google_auth(code=code)
    async with session as session:
        login_users = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()

    assert len(users) == 0
    assert users is not None
    assert login_users is not None


async def test_google_auth__login_exist_user(auth_service, get_db_session):
    code = "fake_code"
    query = insert(UserProfile).values(
        id=EXIST_GOOGLE_USER_ID,
        email=EXIST_GOOGLE_USER_EMAIL
    )

    async with get_db_session as session:
        await session.execute(query)
        await session.commit()

    user_data = await auth_service.google_auth(code=code)


    async with session as session:
        login_users = (await session.execute(select(UserProfile).where(
            UserProfile.id == user_data.user_id))).scalars().first()


    assert login_users.email == EXIST_GOOGLE_USER_EMAIL
    assert login_users.id == EXIST_GOOGLE_USER_ID