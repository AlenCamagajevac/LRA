from flask import Blueprint
from flask_restplus import Api
from .auth import api as auth_api
from .user import api as user_api
from .article import api as article_api
from .notification import api as notification_api


blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='CBC Clusters API',
    version='0.1.0',
    description='Backend API for CBC Clusters platform'
)

# Register resources
api.add_namespace(auth_api, path='/auth')
api.add_namespace(user_api, path='/user')
api.add_namespace(article_api, path='/article')
api.add_namespace(notification_api, path='/notification')
