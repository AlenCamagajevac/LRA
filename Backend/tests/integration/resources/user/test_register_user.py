from pytest import mark, param
from uuid import UUID
from core.enum.role_enum import RoleTypes
from dao.user.user import User
from json import dumps, loads


def test_admin_creates_user(app, seeded_database, admin_access_token_header):
    # Given
    new_user_info = {
        'email': 'test@virtu.ai',
        'name': 'Test User',
        'password': 'password'
    }

    # When
    response = app.test_client().post(
        '/api/user',
        data=dumps(new_user_info),
        headers=admin_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    created_user = User.find_by_email('test@virtu.ai')

    # Then
    assert response.status_code == 201
    assert created_user.uuid == UUID(response_body['uuid'])
    assert not created_user.confirmed
    assert next(role for role in created_user.roles
                if role.role_type == RoleTypes.ADMIN)


def test_non_admin_creates_user(app, seeded_database):
    # Given
    new_user_info = {
        'email': 'test@virtu.ai',
        'name': 'Test User',
        'password': 'password'
    }

    # When
    response = app.test_client().post(
        '/api/user',
        data=dumps(new_user_info),
        content_type='application/json'
    )
    response_body = loads(response.data)

    created_user = User.find_by_email('test@virtu.ai')

    # Then
    assert response.status_code == 201
    assert created_user.uuid == UUID(response_body['uuid'])
    assert not created_user.confirmed
    assert next(role for role in created_user.roles
                if role.role_type == RoleTypes.CLIENT)


@mark.parametrize(
    "new_user_info, expected_status_code",
    [
        param({
            'email': 'invalid email',
            'name': 'Test User'
        }, 400),
        param({
            'email': 'a',
            'name': 'Test User'
        }, 400),
        param({
            'email': 'test@virtu.ai',
            'name': 'a'
        }, 400)
    ]
)
def test_register_user_invalid_form(
        app, seeded_database, admin_access_token_header,
        new_user_info, expected_status_code):
    # Given
    # User info from parameter

    # When
    response = app.test_client().post(
        '/api/user',
        data=dumps(new_user_info),
        headers=admin_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == expected_status_code
    assert 'error' in response_body
