from core.enum.role_enum import RoleTypes
from dao.user.user import User


def test_setting_user_password(new_user: User):
    # Given
    user = new_user

    # When
    user.set_password('password')

    # Then
    assert user.check_password('password')
    assert not user.check_password('wrong_password')
    assert user.password_hash != 'password'


def test_setting_user_role(new_user: User,
                           mock_role_find_by_type_return_client_role):
    # Given
    user = new_user

    # When
    user.add_to_role(RoleTypes.CLIENT)

    # Then
    assert next((role for role in user.roles
                 if role.role_type == RoleTypes.CLIENT))
