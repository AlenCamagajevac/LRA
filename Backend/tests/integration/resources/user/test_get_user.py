from core.enum.role_enum import RoleTypes
from dao.user.user import User
from uuid import uuid4
from json import loads


def test_get_user_details(app, admin_access_token_header, client_user):
    # Given
    # Client user

    # When
    response = app.test_client().get(
        f'/api/user/{client_user.uuid}',
        headers=admin_access_token_header,
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 200
    assert 'email' in response_body
    assert response_body['email'] == client_user.email


def test_get_nonexisting_user_details(app, admin_access_token_header,
                                      client_user):
    # Given
    nonexisting_user_uuid = uuid4()

    # When
    response = app.test_client().get(
        f'/api/user/{nonexisting_user_uuid}',
        headers=admin_access_token_header,
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 404
    assert 'error' in response_body


def test_clients_can_only_get_own_data(app, client_access_token_header,
                                       client_user):
    # Given
    another_user = User(
        email='another-clinet@virtu.ai',
        name='Another test user'
    )
    another_user.add_to_role(RoleTypes.CLIENT)
    another_user.commit()

    # When
    response = app.test_client().get(
        f'/api/user/{another_user.uuid}',
        headers=client_access_token_header,
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 403
    assert 'error' in response_body
