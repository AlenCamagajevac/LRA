from uuid import uuid4, UUID
from json import loads
from datetime import datetime, timedelta


def test_get_article(app, article):
    # Given
    # Article saved in db

    # When
    response = app.test_client().get(
        f'/api/article/{article.uuid}'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 200
    assert 'title' in response_body
    assert response_body['title'] == article.title


def test_get_nonexisting_article(app):
    # Given
    nonexisting_article_uuid = uuid4()

    response = app.test_client().get(
        f'/api/article/{nonexisting_article_uuid}'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 404
    assert 'error' in response_body


def test_get_paginated_articles(app, article):
    # Given
    page = 1
    since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    to = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    sort = 'Descending'

    # When
    response = app.test_client().get(
        f'/api/article?page={page}&since={since}&to={to}&sort={sort}'
    )
    response_body = loads(response.data)

    # Then
    assert response.status_code == 200
    assert 'pages' in response_body
    assert response_body['pages'] == 1
    assert 'items' in response_body
    assert UUID(response_body['items'][0]['uuid']) == article.uuid
    assert 'preview' in response_body['items'][0]
