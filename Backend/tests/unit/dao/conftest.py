from core.enum.role_enum import RoleTypes
from dao.user.role import Role
from pytest import fixture
from dao.user.user import User


@fixture(scope='module')
def new_user():
    return User(
        email='test@virtu.ai',
        name='Test Name'
    )


@fixture(scope='function')
def mock_role_find_by_type_return_client_role(monkeypatch):
    def mock_find_by_type(*args, **kwargs):
        return Role(
            role_type=RoleTypes.CLIENT,
            description="Test role"
        )

    monkeypatch.setattr(Role, 'find_by_type', mock_find_by_type)
