from json.decoder import JSONDecodeError
from pytest import raises
from dao.user.user import User
from json import loads


def test_user_delete(app, admin_access_token_header, client_user):
    # Given
    # Clinet user

    # When
    response = app.test_client().delete(
        f'/api/user/{client_user.uuid}',
        headers=admin_access_token_header
    )

    # Then
    assert response.status_code == 204
    assert not User.find_by_email('test-client@virtu.ai')


def test_user_delete_returns_no_content(app, admin_access_token_header,
                                        client_user):
    # Given
    # Clinet user

    # When
    response = app.test_client().delete(
        f'/api/user/{client_user.uuid}',
        headers=admin_access_token_header
    )

    with raises(JSONDecodeError) as exec_info:
        loads(response.data)

    # Then
    assert "Expecting value" in str(exec_info.value)


def test_client_trying_to_delete_user(app, client_access_token_header,
                                      client_user):
    # Given
    # Clinet user

    # When
    response = app.test_client().delete(
        f'/api/user/{client_user.uuid}',
        headers=client_access_token_header
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 403
    assert 'error' in response_body
