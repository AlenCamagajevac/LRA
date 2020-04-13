from json import loads, dumps


def test_update_user(app, admin_access_token_header, client_user):
    # Given
    update_info = {
        'name': 'Updated Name'
    }

    # When
    response = app.test_client().put(
        f'/api/user/{client_user.uuid}',
        data=dumps(update_info),
        headers=admin_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    updated_user_response = app.test_client().get(
        f'/api/user/{client_user.uuid}',
        headers=admin_access_token_header,
    )
    updated_user = loads(updated_user_response.data)

    # Then
    assert response.status_code == 200
    assert 'name' in response_body
    assert response_body['name'] == 'Updated Name'
    assert response_body['name'] == updated_user['name']


def test_update_user_only_allowed_properties(app, admin_access_token_header,
                                             client_user):
    # Given
    update_info = {
        'email': 'updated-email@belisce.hr'
    }

    # When
    response = app.test_client().put(
        f'/api/user/{client_user.uuid}',
        data=dumps(update_info),
        headers=admin_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 400
    assert 'error' in response_body


def test_only_admin_can_update_user(app, client_access_token_header,
                                    client_user):
    # Given
    update_info = {
        'name': 'Updated Name'
    }

    # When
    response = app.test_client().put(
        f'/api/user/{client_user.uuid}',
        data=dumps(update_info),
        headers=client_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 403
    assert 'error' in response_body
