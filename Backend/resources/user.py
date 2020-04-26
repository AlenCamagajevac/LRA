from schemas.user.user_claims_schema import UserClaimsSchema
from schemas.user.paginated_user_schema import PaginatedUserSchema
from flask import request
from flask import current_app as app
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_optional
from core.responses.error_response import ErrorResponse
from schemas.user.user_schema import UserSchema
from schemas.error.error_response_schema import ErrorResponseSchema
from schemas.user.update_user_schema import UpdateUserSchema
from core.enum.role_enum import RoleTypes
from core.auth.jwt import jwt_required
from core.mail.mail_handler import send_confirmation_token
from dao.user.user import User
from marshmallow import ValidationError
from uuid import UUID

from logging import getLogger

log = getLogger(__name__)

api = Namespace(
    'user', description='User management for virtu.ai platform')

# Api Docs
register_model = api.model('Register model', {
    'email': fields.String(description='user email')
})

user_model = api.model('User created model', {
    'id': fields.Integer(description='id of a created user'),
    'email': fields.String(description='email of created user')
})


@api.route('')
class UsersResource(Resource):
    user_schema = UserSchema()
    user_claims_schema = UserClaimsSchema()

    @api.expect(register_model)
    @api.response(201, 'Created', user_model)
    @jwt_optional
    def post(self):
        # Map request body to user model
        try:
            user = self.user_schema.load(api.payload)
        except ValidationError as err:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details=err.messages,
                error='validation errors'
            ))
            log.info(
                f'Validation errors during user creation: {error_response}')
            return error_response, 400

        # Check if user with same email already exists
        if User.find_by_email(user.email) is not None:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'user': ['User with provided email already exists']
                },
                error='duplicate email'
            ))
            log.info(f'trying to create user with existing email {user.email}')
            return error_response, 400

        # If caller was ADMIN create ADMIN if caller was CLIENT create CLIENT
        user_claims = self.user_claims_schema.load(get_jwt_claims())
        if user_claims.is_admin():
            user.add_to_role(RoleTypes.ADMIN)
        else:
            user.add_to_role(RoleTypes.CLIENT)

        # Send confirmation mail that user was created
        if app.config['REQUIRE_MAIL_CONFIRMATION']:
            send_confirmation_token(user.email)
        else:
            user.confirm_account()

        # Save model to DB
        user.commit()

        # Map saved user to response body
        log.info(f'Sucessfuly created new user')
        return self.user_schema.dump(user), 201

    # GET api/user?page=1 - gets all users
    @jwt_required([RoleTypes.ADMIN])
    def get(self):

        # Get optional page number
        try:
            page = int(request.args.get('page'))
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

        # Find all users on that page
        users = User.find_all_users(page or 1, 20)

        # Map users to schema
        paginated_user_schema = PaginatedUserSchema()
        return paginated_user_schema.dump(users), 200


@api.route('/<string:uuid>')
class UserResourceList(Resource):
    error_schema = ErrorResponseSchema()
    user_claims_schema = UserClaimsSchema()
    user_schema = UserSchema()

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

    # GET api/user/1 - get details for specific users
    @jwt_required([RoleTypes.ADMIN, RoleTypes.CLIENT])
    def get(self, uuid):
        # Try to find user
        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.incorrect_uuid(uuid), 404

        user = User.find_by_uuid(uuid)

        # If user is requesting details for another user
        user_claims = self.user_claims_schema.load(get_jwt_claims())
        if user_claims.is_client() and user.uuid != UUID(get_jwt_identity()):
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'Access to that resource is forbidden'
                },
                error='User not found'
            ))
            log.info(
                f'User not found: {error_response}')
            return error_response, 403

        # If there is no user with given id
        if not user:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'User with {uuid} uuid does not exist'
                },
                error='User not found'
            ))
            log.info(
                f'User not found: {error_response}')
            return error_response, 404

        # Return user
        return self.user_schema.dump(user), 200

    # DELETE api/user/1 - delete specific user
    @jwt_required([RoleTypes.ADMIN])
    def delete(self, uuid):
        # Try to find user
        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.incorrect_uuid(uuid), 404

        user = User.find_by_uuid(uuid)

        # If there is no user with given id
        if not user:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'User with {uuid} uuid does not exist'
                },
                error='User not found'
            ))
            log.info(
                f'User not found: {error_response}')
            return error_response, 404

        # delete user
        user.remove()

        return '', 204

    @jwt_required([RoleTypes.ADMIN])
    def put(self, uuid):
        # Map input data
        try:
            user_update_schema = UpdateUserSchema()
            update_info = user_update_schema.load(api.payload)
        except ValidationError as err:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details=err.messages,
                error='validation errors'
            ))
            log.info(
                f'Validation errors during user update: {error_response}')
            return error_response, 400

        # Try to find user
        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.incorrect_uuid(uuid), 404

        user = User.find_by_uuid(uuid)

        # If there is no user with given id
        if not user:
            error_schema = ErrorResponseSchema()
            error_response = error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'User with {uuid} uuid does not exist'
                },
                error='User not found'
            ))
            log.info(
                f'User not found: {error_response}')
            return error_response, 404

        # update user properties
        for key, value in update_info.items():
            setattr(user, key, value)
        user.commit()

        # return updated user
        return self.user_schema.dump(user), 200
