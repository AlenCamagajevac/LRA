class Config():
    DEBUG = False
    TESTING = False

    JWT_SECRET_KEY = "Belisce-JWT-SecretKey"
    MAIL_SECRET_KEY = "Mail-Secret-Key"

    SALT = "Some-Random-Salt"

    PROPAGATE_EXCEPTIONS = True

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'alen.camagajevac@gmail.com'
    MAIL_PASSWORD = 'pass'

    # mail accounts
    MAIL_DEFAULT_SENDER = ('no-reply', 'no-reply@belisce.hr')

    # confirmation endpoint
    MAIL_CONFIRMATION_ENDPOINT = 'localhost:5000/api/auth/confirmation'
    REQUIRE_MAIL_CONFIRMATION = True

    APP_ARTICLE_CATEGORIES = [
        'Vidljivost', 'Ekonomski trendovi', 'komunikacija i networking']

    # Notification settings
    ARTICLE_DETAILS_ENDPOINT = 'localhost:5000/api/article'


class ProductionConfig(Config):
    DEBUG = False

    LOG_CONFIG_FILE = 'logging.development.yaml'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    LOG_CONFIG_FILE = 'logging.development.yaml'

    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "password"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "belisce"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True

    LOG_CONFIG_FILE = 'logging.development.yaml'

    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "password"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "belisce-test"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
