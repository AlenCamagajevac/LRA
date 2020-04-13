
from dao.user.role import Role
from core.enum.role_enum import RoleTypes
from dao.user.user import User
from core.seed_data.database_seed import DatabaseSeeder


def test_database_seeder_inserts_admin(app):
    # Given
    # seeded_database

    # When
    user = User.find_by_email('admin@belisce.hr')

    # Then
    assert user
    assert user.email == 'admin@belisce.hr'
    assert any(role for role in user.roles if
               role.role_type == RoleTypes.ADMIN)


def test_database_seeder_inserts_roles(app):
    # Given
    # seeded_database

    # When
    admin_role = Role.find_by_type(RoleTypes.ADMIN)
    client_role = Role.find_by_type(RoleTypes.CLIENT)

    # Then
    assert admin_role
    assert admin_role.role_type == RoleTypes.ADMIN
    assert client_role
    assert client_role.role_type == RoleTypes.CLIENT
