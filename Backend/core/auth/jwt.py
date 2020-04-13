from functools import wraps
from schemas.user.user_claims_schema import UserClaimsSchema
from typing import List
from schemas.error.error_response_schema import ErrorResponseSchema
from core.responses.error_response import ErrorResponse
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from core.enum.role_enum import RoleTypes
from logging import getLogger

log = getLogger(__name__)


def jwt_required(required_roles: List[RoleTypes]):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_claims_schema = UserClaimsSchema()
            user_claims = user_claims_schema.load(get_jwt_claims())

            # if user claims contains any required role
            if user_claims.contains_any_roles(required_roles):
                return fn(*args, **kwargs)
            # Otherwise forbidd access
            else:
                error_schema = ErrorResponseSchema()
                error_response = error_schema.dump(ErrorResponse(
                    details={
                        'jwt': 'User not in required role'
                    },
                    error='forbidden action'
                ))
                log.info(
                    f'Forbidden action: {error_response}')
                return error_response, 403

        return wrapper

    return decorator
