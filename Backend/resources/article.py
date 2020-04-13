from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from core.responses.error_response import ErrorResponse
from core.enum.role_enum import RoleTypes
from core.auth.jwt import jwt_required
from core.enum.order_enum import OrderType
from marshmallow import ValidationError
from schemas.article.create_article_schema import CreateArticleSchema
from dao.article.article import Article
from dao.user.user import User
from schemas.article.article_schema import ArticleSchema
from schemas.article.pagintaed_article_schema import PaginatedArticleSchema
from schemas.article.update_article_schema import UpdateArticleSchema
from uuid import UUID
from schemas.error.error_response_schema import ErrorResponseSchema
from core.utils.date_converter import toDate
from task_queue.tasks.mail_handler import send_notification_mail

from logging import getLogger

log = getLogger(__name__)

api = Namespace(
    'article', description='Article endpoints for CBC Clusters platform')

# Api Docs
create_article_model = api.model('Create article model', {
    'content': fields.String(description='article content')
})

article_model = api.model('Article model', {
    'id': fields.Integer(description='article id'),
    'content': fields.String(description='content of an article'),
    'created_date': fields.DateTime(description='Date of article creation')
})


@api.route('')
class ArticlesResource(Resource):
    article_schema = ArticleSchema()
    paginated_articles_schema = PaginatedArticleSchema()
    error_schema = ErrorResponseSchema()
    create_article_schema = CreateArticleSchema()
    error_schema = ErrorResponseSchema()

    # POST api/article - create new article
    @api.expect(create_article_model)
    @api.response(201, 'Created', article_model)
    @jwt_required([RoleTypes.ADMIN])
    def post(self):

        # Find user trying to save article
        user = User.find_by_uuid(get_jwt_identity())

        # Check if article is valid
        try:
            article = self.create_article_schema.load(api.payload)
        except ValidationError as err:
            error_response = self.error_schema.dump(ErrorResponse(
                details=err.messages,
                error='validation errors'
            ))
            log.info(
                f'Validation errors during article creation: {error_response}')
            return error_response, 400

        # Add user to article
        article.user = user

        # Save article
        article.commit()

        # Send notification that there is new article
        users_to_notify = User.find_with_mail_notifications_enabled()
        send_notification_mail.delay(
            [user.email for user in users_to_notify],
            article.title,
            article.uuid
        )

        # Return article model
        return self.article_schema.dump(article), 201

    # GET api/article - get all articles (filtered by query)
    def get(self):
        # Get optional page number
        try:
            filter_params = {
                'per_page': request.args.get('per_page', default=10, type=int),
                'page': request.args.get('page', default=1, type=int),
                'from': request.args.get('from', default=None, type=toDate),
                'to': request.args.get('to', default=None, type=toDate),
                'sort': request.args.get(
                    'sort', default=OrderType.DESCENDING, type=OrderType)
            }
        except ValueError:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'page': 'Page should be number'
                },
                error='validation errors'
            ))
            log.info(
                f'Invalid page query argument: {error_response}')
            return error_response, 400

        # Find all articles on that page
        articles = Article.find_all_articles(filter_params)

        # Map articles to schema
        return self.paginated_articles_schema.dump(articles), 200


@api.route('/<string:uuid>')
class ArticleResource(Resource):
    error_schema = ErrorResponseSchema()
    article_schema = ArticleSchema()
    update_article_schema = UpdateArticleSchema()

    def incorrect_uuid(self, uuid):
        error_response = self.error_schema.dump(ErrorResponse(
            details={
                'uuid': f'Badly formed uuid: {uuid}'
            },
            error='uuid format error'
        ))
        log.info(
            f'uuid format error: {error_response}')
        return error_response

    # GET api/article/1 - get details for article
    def get(self, uuid):
        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.incorrect_uuid(uuid), 404

        article = Article.find_by_uuid(uuid)
        if not article:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'Article with {uuid} uuid does not exist'
                },
                error='Article not found'
            ))
            log.info(
                f'Article not found: {error_response}')
            return error_response, 404

        return self.article_schema.dump(article), 200

    # PUT api/article/1 - update article
    @jwt_required([RoleTypes.ADMIN])
    def put(self, uuid):
        # Map input data
        try:
            update_info = self.update_article_schema.load(api.payload)
        except ValidationError as err:
            error_response = self.error_schema.dump(ErrorResponse(
                details=err.messages,
                error='validation errors'
            ))
            log.info(
                f'Validation errors during article update: {error_response}')
            return error_response, 400

        # Try to find article
        article = Article.find_by_uuid(uuid)
        if not article:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'Article with {uuid} uuid does not exist'
                },
                error='Article not found'
            ))
            log.info(
                f'Article not found: {error_response}')
            return error_response, 404

        # Update article
        for key, value in update_info.items():
            setattr(article, key, value)
        article.commit()

        return self.article_schema.dump(article), 200

    # DELETE api/article/1 - delete article
    @jwt_required([RoleTypes.ADMIN])
    def delete(self, uuid):
        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.incorrect_uuid(uuid), 404

        article = Article.find_by_uuid(uuid)
        if not article:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'Article with {uuid} uuid does not exist'
                },
                error='Article not found'
            ))
            log.info(
                f'Article not found: {error_response}')
            return error_response, 404

        article.remove()

        return '', 204
        pass
