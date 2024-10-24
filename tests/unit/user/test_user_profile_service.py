from app.users.user_profile.schema import UserBaseSchema
from app.users.user_profile.service import UserService


async def test_create_user(user_service_mock: UserService):
    body = UserBaseSchema(username='test@example.com', name='Test User', password='password')
    user = await user_service_mock.create_user(user=body)

    assert user.user_id is not None
