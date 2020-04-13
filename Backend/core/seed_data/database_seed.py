from sqlalchemy.exc import IntegrityError

from dao.user.user import User
from dao.user.role import Role
from dao.article.category import Category
from core.enum.role_enum import RoleTypes
from datetime import datetime

from logging import getLogger

log = getLogger()


class DatabaseSeeder():
    def seed_application_users(self):
        try:
            admin_role = Role(
                role_type=RoleTypes.ADMIN,
                description="Admin role for belisce dev agency platform"
            )
            admin_role.commit()

            client_role = Role(
                role_type=RoleTypes.CLIENT,
                description="Client role for belisce dev agency platform"
            )
            client_role.commit()

            # Define application users
            admin_user = User(
                # TODO load from config
                email="admin@belisce.hr",
                confirmed=True,
                confirmed_date=datetime.utcnow()
            )

            admin_user.set_password('password')
            admin_user.add_to_role(RoleTypes.ADMIN)
            admin_user.commit()

        except IntegrityError:
            log.info('Data is already present in database')
            pass

    def seed_article_categories(self, app_article_categories):
        for c in app_article_categories:
            category = Category(name=c)
            category.commit()
        pass

    def init_app(self, app):
        @app.cli.command("seed-database")
        def seed_database():
            self.seed_application_users()

            app_article_categories = app.config['APP_ARTICLE_CATEGORIES']
            self.seed_article_categories(app_article_categories)
