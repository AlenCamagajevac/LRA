from json import dumps, loads
from core.enum.role_enum import RoleTypes
from dao.user.user import User
from flask_jwt_extended import decode_token
from uuid import UUID


def test_user_login_successful(app):
    # Given
    user = User(email='test@virtu.ai', name='test user')
    user.add_to_role(RoleTypes.CLIENT)
    user.set_password('password')
    user.confirm_account()
    user.commit()

    login_info = {
        'email': 'test@virtu.ai',
        'password': 'password'
    }

    # When
    response = app.test_client().post(
        '/api/auth/login',
        data=dumps(login_info),
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 200
    assert 'access_token' in response_body
    assert 'refresh_token' in response_body


def test_user_login_incorrect(app):
    # Given
    user = User(email='test@virtu.ai', name='test user')
    user.add_to_role(RoleTypes.CLIENT)
    user.set_password('password')
    user.confirm_account()
    user.commit()

    login_info = {
        'email': 'test@virtu.ai',
        'password': 'wrong_password'
    }

    # When
    response = app.test_client().post(
        '/api/auth/login',
        data=dumps(login_info),
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 400
    assert response_body['error'] == 'wrong password'


def test_user_login_unconfirmed(app):
    # Given
    user = User(email='test@virtu.ai', name='test user')
    user.add_to_role(RoleTypes.CLIENT)
    user.set_password('password')
    user.commit()

    login_info = {
        'email': 'test@virtu.ai',
        'password': 'password'
    }

    # When
    response = app.test_client().post(
        '/api/auth/login',
        data=dumps(login_info),
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 400
    assert response_body['error'] == 'user not confirmed'


def test_access_token_issued_from_valid_refresh_token(
        app, client_user, client_refresh_token_header):
    # Given
    # Client_user

    # When
    response = app.test_client().get(
        '/api/auth/login/refresh',
        headers=client_refresh_token_header
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 200
    assert 'access_token' in response_body


def test_valid_identity_in_access_token(
        app, client_user, client_refresh_token_header):
    # Given
    # client_user

    # When
    response = app.test_client().get(
        '/api/auth/login/refresh',
        headers=client_refresh_token_header
    )
    response_body = loads(response.data)

    # Then
    assert 'access_token' in response_body
    decoded_token = decode_token(response_body['access_token'])
    assert UUID(decoded_token['identity']) == client_user.uuid
