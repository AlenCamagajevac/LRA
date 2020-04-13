from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity)
from marshmallow import ValidationError
from uuid import UUID
from dao.user.user import User
from core.responses.error_response import ErrorResponse
from core.dto.auth.token_dto import TokenDto
from core.utils.confirmation_mail_handler import ConfirmationMailHandler
from core.errors.invalid_confirmation_token import InvalidConfirmationToken
from schemas.auth.login_schema import LoginSchema
from schemas.auth.token_schema import TokenSchema
from schemas.error.error_response_schema import ErrorResponseSchema

from logging import getLogger

log = getLogger(__name__)

api = Namespace('auth', description='Authentication for virtu.ai platform')

# Api Docs
login_model = api.model('Login form', {
    'email': fields.String(description='user email'),
    'password': fields.String(description='user password')
})

login_response = api.model('Login response', {
    'access_token': fields.String(description='jwt token'),
    'refresh_token': fields.String(description='refresh token')
})

token_refresh_response = api.model('Token refresh response', {
    'access_token': fields.String(description='jwt token')
})


@api.route('/login')
class LoginResource(Resource):
    login_schema = LoginSchema()
    error_schema = ErrorResponseSchema()
    token_schema = TokenSchema()

    @api.expect(login_model)
    @api.response(200, 'Success', login_response)
    def post(self):
        # Serialize login model
        try:
            login_dto = self.login_schema.load(api.payload)
        except ValidationError as err:
            error_response = self.error_schema.dump(ErrorResponse(
                details=err.messages,
                error='validation errors'
            ))
            log.info(f'Validation errors during login: {error_response}')
            return error_response, 400

        # Find user in database
        user = User.find_by_email(login_dto.email)
        if not user:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'user': [f'There is no user with {login_dto.email} email']
                },
                error='not existing user'
            ))
            log.info(f'Trying to log in non existing user: {error_response}')
            return error_response, 404

        # Chcek if user is confirmed
        if not user.confirmed:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'user': [f'User {user.name} is unconfirmed']
                },
                error='user not confirmed'
            ))
            log.info(f'Trying to log in unconfirmed user: {error_response}')
            return error_response, 400

        # Check user password
        if not user.check_password(login_dto.password):
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'password': ['You provided wrong password']
                },
                error='wrong password'
            ))
            log.info(f'Wrong password used during login: {error_response}')
            return error_response, 400

        # Create JWT from user data
        token = TokenDto(create_access_token(identity=user),
                         create_refresh_token(identity=user))

        # Return token
        log.info('User login sucessful')
        return self.token_schema.dump(token), 200


@api.route('/login/refresh')
class RefreshTokenResource(Resource):
    @api.response(200, 'Success', token_refresh_response)
    @jwt_refresh_token_required
    def get(self):
        # Get identity of user from refresh token
        current_user_uuid = get_jwt_identity()

        # Try to find user in db
        user = User.find_by_uuid(UUID(current_user_uuid))
        if not user:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'user': ['There is no user with given email']
                },
                error='not existing user'
            ))
            log.warn(
                f'Non existing user {current_user_uuid}' +
                f' trying to refresh token: {error_response}')
            return error_response, 404

        # Generate new access token with user
        token = TokenDto(create_access_token(identity=user))

        # Return only access token
        token_schema = TokenSchema(only=['access_token'])
        log.info(f'Access token refresh successful')
        return token_schema.dump(token), 200


@api.route('/confirmation/<string:token>')
class ConfirmationResource(Resource):
    error_schema = ErrorResponseSchema()

    def get(self, token):
        # Confirm token
        try:
            email = ConfirmationMailHandler.confirm_token(token)
        except InvalidConfirmationToken:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'token': f'{email} is invalid or expired'
                },
                error='Invalid or expired token'
            ))
            log.info(
                f'Invalid token: {error_response}')
            return error_response, 403

        # Find user that token belongs to
        user = User.find_by_email(email)
        if not user:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'user': [f'There is no user with {email} email']
                },
                error='not existing user'
            ))
            log.info(f'Trying to confirm non existing user: {error_response}')
            return error_response, 404

        # Check if user was already confirmed
        if user.confirmed:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'user': [f'User "{user.name}" is already confirmed']
                },
                error='User already confirmed'
            ))
            log.info(
                f'Trying to confirm already confirmed user: {error_response}')
            return error_response, 404

        # Confirm user
        user.confirm_account()
        user.commit()

        return '', 204
