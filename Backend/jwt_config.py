from schemas.user.user_claims_schema import UserClaimsSchema
from flask_jwt_extended import JWTManager
from core.responses.error_response import ErrorResponse
from schemas.error.error_response_schema import ErrorResponseSchema
from dao.user.user import User

error_schema = ErrorResponseSchema()


def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_jwt(user: User):
        schema = UserClaimsSchema()
        return schema.dump(user)

    @jwt.user_identity_loader
    def user_identity_lookup(user: User):
        return user.uuid

    @jwt.expired_token_loader
    def expired_token_callback():
        return error_schema.dump(ErrorResponse(
            details={
                'token': ['Token has expired']
            },
            error='expired_token'
        )), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return error_schema.dump(ErrorResponse(
            details={
                'token': ['Signature verification failed']
            },
            error='invalid_token'
        )), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return error_schema.dump(ErrorResponse(
            details={
                'token': ['Request does not contain an access token']
            },
            error='authorization_required'
        )), 401
