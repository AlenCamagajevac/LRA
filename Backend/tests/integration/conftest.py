from core.enum.role_enum import RoleTypes
from dao.user.user import User
from dao.article.article import Article
from dao.article.category import Category
from db import db
from belisce import create_app
from pytest import fixture
from flask_jwt_extended import create_access_token, create_refresh_token
from core.seed_data.database_seed import DatabaseSeeder
from task_queue.make_celery import celery
from task_queue.init_celery import init_celery


@fixture(autouse=True, scope='function')
def app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@fixture(scope='function')
def celery_parameters(app):
    init_celery(celery, app)
    return {
        'task_cls': celery.Task,
        'strict_typing': False,
    }


@fixture(scope='function')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379/1',
        'result_backend': 'redis://localhost:6379/0'
    }


@fixture(autouse=True, scope='function')
def seeded_database():
    seeder = DatabaseSeeder()
    seeder.seed_application_users()


@fixture(scope='function')
def admin_user(seeded_database):
    admin_user = User(email='test-admin@virtu.ai')
    admin_user.add_to_role(RoleTypes.ADMIN)
    admin_user.commit()
    return admin_user


@fixture(scope='function')
def client_user(seeded_database):
    client_user = User(email='test-client@virtu.ai')
    client_user.add_to_role(RoleTypes.CLIENT)
    client_user.commit()
    return client_user


@fixture(scope='function')
def category(seeded_database):
    category = Category(name="Test")
    category.commit()
    return category


@fixture(scope='function')
def article(seeded_database, admin_user, category):
    article = Article(
        title="Test article",
        content="Test content",
        user=admin_user,
        category=category
    )
    article.commit()
    return article


@fixture
def admin_access_token_header(admin_user):
    access_token = create_access_token(identity=admin_user)
    return {
        'Authorization': f'Bearer {access_token}'
    }


@fixture
def client_access_token_header(client_user):
    access_token = create_access_token(identity=client_user)
    return {
        'Authorization': f'Bearer {access_token}'
    }


@fixture
def admin_refresh_token_header(admin_user):
    access_token = create_refresh_token(identity=admin_user)
    return {
        'Authorization': f'Bearer {access_token}'
    }


@fixture
def client_refresh_token_header(client_user):
    access_token = create_refresh_token(identity=client_user)
    return {
        'Authorization': f'Bearer {access_token}'
    }
