import logging
import logging.config
import yaml

from flask import Flask
from flask_migrate import Migrate
from jwt_config import setup_jwt
from resources import blueprint as api_blueprint
from db import db
from core.seed_data.database_seed import DatabaseSeeder
from core.logging.access_log import init_access_logger
from core.metrics.prometheus import metrics
from mail import mail

log = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    # Load config
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Initialize logs
    logging.config.dictConfig(
        yaml.load(
            open(app.config["LOG_CONFIG_FILE"]), Loader=yaml.FullLoader)
    )
    init_access_logger(app)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Initialize jwt
    setup_jwt(app)

    # Initialize database
    db.init_app(app)

    # Initialize migrations
    Migrate(app, db)

    # Seed database data
    seeder = DatabaseSeeder()
    seeder.init_app(app)

    # Initialize metrics
    try:
        metrics.init_app(app)
    except ValueError:
        log.info('Metrics already initialized')

    # Initialize mail
    mail.init_app(app)

    return app
