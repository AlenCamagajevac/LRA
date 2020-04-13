from dao.article.article import Article
from json import loads, dumps
from uuid import UUID


def test_admin_creates_article(app, seeded_database, admin_access_token_header, category, admin_user):
    # Given
    new_article_info = {
        'title': 'Test Title',
        'content': 'Test Content',
        'category_uuid': str(category.uuid)
    }

    # When
    response = app.test_client().post(
        '/api/article',
        data=dumps(new_article_info),
        headers=admin_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    created_article = Article.find_by_uuid(response_body['uuid'])

    # Then
    assert response.status_code == 201
    assert created_article.uuid == UUID(response_body['uuid'])
    assert UUID(response_body['category']['uuid']) == category.uuid
    assert UUID(response_body['user']['uuid']) == admin_user.uuid


def test_client_creates_article(app, seeded_database, client_access_token_header, category):
    # Given
    new_article_info = {
        'title': 'Test Title',
        'content': 'Test Content',
        'category_uuid': str(category.uuid)
    }

    # When
    response = app.test_client().post(
        '/api/article',
        data=dumps(new_article_info),
        headers=client_access_token_header,
        content_type='application/json'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 403
    assert 'error' in response_body
    assert response_body['details']['jwt'] == "User not in required role"
